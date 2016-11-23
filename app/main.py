import json
import flaskext.couchdb
from flask import Flask, request
from jsonschema import validate, Draft4Validator

from app.model import Item
from schematics.exceptions import ValidationError
from app.utils import prepare_item_to_return, get_db, get_cpv_schema

main_app = Flask(__name__)


@main_app.route('/items', methods=['POST'])
def create_item():
    db = get_db()
    data = json.loads(request.data.decode('utf-8'))
    try:
        schema, save_cpv, version = get_cpv_schema(data['data']['cpv'], data['data']['properties'].get('version', 'last'))
    except FileNotFoundError:
        return json.dumps({'error': 'Schema not found'}), 422
    if schema:  # validate if have schema
        try:
            Draft4Validator(schema).validate(data['data']['properties']['props'])
        except Exception as exc:
            return str(exc), 422
        data['data']['properties']['props'] = json.dumps(data['data']['properties']['props'])
        data['data']['properties']['version'] = version
        data['data']['properties']['save_cpv'] = save_cpv
    if 'properties' in data['data'] and not schema:
        return json.dumps({"error": "We can't save properties because json schema wasn't found."})
    item = Item(data['data'])
    try:
        item.validate()
    except ValidationError as ex:
        return json.dumps(ex.messages)
    else:
        item.store(db)
    return json.dumps(prepare_item_to_return(item))


@main_app.route('/items/<post_id>/', methods=['GET'])
def get_or_edit_item(post_id):
    """ get item """
    item = Item.load(get_db(), post_id)
    item_data = item.serialize()
    if item_data['properties']:
        schema, code, _ = get_cpv_schema(item_data['properties']['save_cpv'], item_data['properties']['version'])
        if schema:  # validate if have schema
            try:
                json_props = json.loads(item_data['properties']['props'])
                Draft4Validator(schema).validate(json_props)
            except Exception as exc:
                return str(exc), 422
            item_data['properties']['props'] = json_props
    return json.dumps(item_data)


@main_app.route('/items/<post_id>/', methods=['PATCH'])
def edit_item(post_id):
    """ Edit item """
    item = Item.load(get_db(), post_id)
    data = json.loads(request.data.decode('utf-8'))
    if 'properties' in data['data'] and 'props' in data['data']['properties']:
        data['data']['properties']['props'] = json.dumps(data['data']['properties']['props'])
    item.import_data(data['data'])
    item_data = item.serialize()
    try:
        schema, code, version = get_cpv_schema(item.cpv, version=item_data['properties']['version'])
    except FileNotFoundError:
        return json.dumps({'error': 'Schema not found'}), 422
    if schema:  # validate if have schema
        try:
            validate(json.loads(item.properties.props), schema)
        except Exception as exc:
            return exc.message, 422
        item.properties.version = version
        item.properties.save_cpv = code
    item.store(get_db())
    return json.dumps(prepare_item_to_return(item))


"""
Flask main
"""
if __name__ == "__main__":
    main_app.config.update(DEBUG=True)
    manager = flaskext.couchdb.CouchDBManager()
    manager.setup(main_app)
    manager.sync(main_app)
    main_app.run(host='0.0.0.0', port=5000)
