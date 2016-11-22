from schematics.types import StringType
from schematics.types.compound import PolyModelType
from couchdb_schematics.document import SchematicsDocument


LAST_VERSION = '001'


class BaseSchema(SchematicsDocument):
    """ BaseSchema model """
    version = StringType(default=LAST_VERSION)
    props = StringType()  # here we will save all properties


class Item(SchematicsDocument):
    """ Base model for schema validation """
    name = StringType(max_length=200)
    cpv = StringType(max_length=10)
    properties = PolyModelType(BaseSchema)
