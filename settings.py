from common.db import Storage
from os import environ

db_user = environ["DB_USER"]
db_password = environ["DB_PASSWORD"]
db_host = environ["DB_HOST"]
db_port = environ["DB_PORT"]
db_resource = environ["DB_RESOURCE"]

db_uri = "postgresql://%s:%s@%s:%s/%s" % (db_user, db_password, db_host,\
        db_port, db_resource)
storage = Storage(db_uri)

