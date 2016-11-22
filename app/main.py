import json
import os.path
import flaskext.couchdb
from flask import Flask, g, request
from jsonschema import validate, Draft4Validator

from app.model import Item
from schematics.exceptions import ValidationError
from app.utils import prepare_item_to_return, get_db, get_cpv_schema

main_app = Flask(__name__)


@main_app.route('/items', methods=['POST'])
def create_item():
    db = get_db()
    data = json.loads(request.data.decode('utf-8'))
    schema = get_cpv_schema(data['data']['cpv'], data['data']['properties']['version'] or 1)
    if schema:  # validate if have schema
        try:
            Draft4Validator(schema).validate(data['data']['properties']['props'])
        except Exception as exc:
            return str(exc), 422
        data['data']['properties']['props'] = json.dumps(data['data']['properties']['props'])
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


@main_app.route('/items/<post_id>/', methods=['GET', 'PATCH'])
def get_or_edit_item(post_id):
    item = Item.load(get_db(), post_id)
    item_data = item.serialize()
    if request.method == 'GET':
        schema = get_cpv_schema(item_data['cpv'])
        if schema:  # validate if have schema
            item_data['properties']['props'] = json.loads(item_data['properties']['props'])
        return json.dumps(item_data)
    elif request.method == 'PATCH':
        db = get_db()
        data = json.loads(request.data.decode('utf-8'))
        props_str = item_data['properties']['props']
        props = json.loads(props_str)
        props.update(data['data']['properties']['props'])
        schema = get_cpv_schema(item.cpv, version=item.properties.version)
        if schema:  # validate if have schema
            try:
                validate(props, schema)
            except Exception as exc:
                return exc.message, 422
        data['data']['properties']['props'] = json.dumps(props)
        item.import_data(data['data'])
        item.store(db)
        return json.dumps(prepare_item_to_return(item))
    else:
        return "", 405


"""
Flask main
"""
if __name__ == "__main__":
    main_app.config.update(DEBUG=True)
    manager = flaskext.couchdb.CouchDBManager()
    manager.setup(main_app)
    manager.sync(main_app)
    main_app.run(host='0.0.0.0', port=5000)
