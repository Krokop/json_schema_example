import json
import os
from re import compile

from flask import g

from couchdb import Server
from app.setttings import COUCHDB_URL

VERSION_RE = compile(r'schema_(?P<version>\d+).json')


def prepare_item_to_return(item):
    """ Return item serialization """
    item_ser = item.serialize()
    if 'properties' in item_ser:
        item_ser['properties']['props'] = json.loads(item_ser['properties']['props'])
    return item_ser


def make_cav_dir_path(cav_code):
    """ Make path to shema directory """
    if len(cav_code) == 2:
        return "schemas/{start}".format(start=cav_code[:2])
    return "schemas/{start}/{list}".format(start=cav_code[:2], list='/'.join(list(cav_code[2:])))


def get_schema_path(schema_path_dir, version):
    if version == 'last':
        return "{dir_path}/{file_name}".format(dir_path=schema_path_dir, file_name=os.listdir(schema_path_dir)[-1])
    else:
        return "{dir_path}/schema_{version:0>3}.json".format(dir_path=schema_path_dir, version=version)


def get_cpv_schema(cpv_code, version="last"):
    """ Return json schema if we can find it by cpv code """
    cpv_code_copy = cpv_code
    while True:
        schema_path = make_cav_dir_path(cpv_code_copy)
        if os.path.isdir(schema_path):
            break
        if len(cpv_code_copy) == 1:
            break
        cpv_code_copy = cpv_code_copy[:-1]
    if len(cpv_code_copy) > 1:
        schema_path = get_schema_path(schema_path, version)
        with open(schema_path, 'rb') as schema_file:
            schema_text = schema_file.read().decode('utf-8')
            return json.loads(schema_text), cpv_code_copy, VERSION_RE.search(schema_path).groupdict()['version']
    return None, None, None


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