import json
import os.path
import flaskext.couchdb
from flask import Flask, g, request
from jsonschema import validate
from couchdb import Server
from app.model import BaseSchema, Item, LAST_VERSION

main_app = Flask(__name__)


def get_cpv_schema(cpv_code, version=LAST_VERSION):
    cpv_start = cpv_code[:4]
    path = "./schemas/{cpv}_{version}.json".format(cpv=cpv_start, version=version)
    if os.path.isfile(path):
        with open(path, 'rb') as schema_file:
            schema_text = schema_file.read().decode('utf-8')
            return json.loads(schema_text)
    return


@main_app.route('/items', methods=['POST'])
def create_item():
    db = get_db()
    data = json.loads(request.data.decode('utf-8'))
    schema = get_cpv_schema(data['data']['cpv'])
    if schema:  # validate if have schema
        try:
            validate(data['data']['properties']['props'], schema)
        except Exception as exc:
            return exc.message
        data['data']['properties']['props'] = json.dumps(data['data']['properties']['props'])
    item = Item(data['data'])
    item.store(db)
    return json.dumps(item.serialize())


@main_app.route('/items/<post_id>/', methods=['GET', 'PUT'])
def get_or_edit_item(post_id):
    item = Item.load(get_db(), post_id)
    item_data = item.serialize()
    if request.method == 'GET':
        schema = get_cpv_schema(item_data['cpv'])
        if schema:  # validate if have schema
            item_data['properties']['props'] = json.loads(item_data['properties']['props'])
        return json.dumps(item_data)
    else:
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
                return exc.message
        data['data']['properties']['props'] = json.dumps(props)
        item.import_data(data['data'])
        item.store(db)
        item_ser = item.serialize()
        item_ser['properties']['props'] = json.loads(item_ser['properties']['props'])
        return json.dumps(item_ser)


def get_db():
    """ Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        server = Server('http://admin:admin@127.0.0.1:9000/')
        if 'web' not in server:
            server.create('web')
        db = server['web']
        g.db = db
    return g.db

"""
Flask main
"""
if __name__ == "__main__":
    main_app.config.update(DEBUG=True)
    manager = flaskext.couchdb.CouchDBManager()
    manager.setup(main_app)
    manager.sync(main_app)
    main_app.run(host='0.0.0.0', port=5000)
