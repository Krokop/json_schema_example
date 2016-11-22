import json
import os

from couchdb import Server
from app.setttings import COUCHDB_URL


def prepare_item_to_return(item):
    """ Return item serialization """
    item_ser = item.serialize()
    if 'properties' in item_ser:
        item_ser['properties']['props'] = json.loads(item_ser['properties']['props'])
    return item_ser


def make_cav_path(cav_code, version):
    if len(cav_code) == 2:
        return "schemas/{start}/schema_{version:0>3}.json".format(start=cav_code[:2], version=version)
    return "schemas/{start}/{list}/schema_{version:0>3}.json".format(start=cav_code[:2],
                                                                     list='/'.join(list(cav_code[2:])),
                                                                     version=version)


def get_cpv_schema(cpv_code, version="001"):
    """ Return json schema if we can find it by cpv code """
    cpv_code_copy = cpv_code
    while True:
        schema_path = make_cav_path(cpv_code_copy, version)
        print("schema_path", schema_path)
        if os.path.isfile(schema_path):
            break
        if len(cpv_code_copy) == 1:
            break
        cpv_code_copy = cpv_code_copy[:-1]
    if len(cpv_code_copy) > 1:
        with open(schema_path, 'rb') as schema_file:
            schema_text = schema_file.read().decode('utf-8')
            return json.loads(schema_text)
    return


def get_db():
    """ Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        server = Server(COUCHDB_URL)
        if 'web' not in server:
            server.create('web')
        db = server['web']
        g.db = db
    return g.db