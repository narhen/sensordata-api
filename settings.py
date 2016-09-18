from os import environ

db_user = environ["DB_USER"]
db_password = environ["DB_PASSWORD"]
db_host = environ["DB_HOST"]
db_port = int(environ["DB_PORT"])
db_resource = environ["DB_RESOURCE"]
jwt_secret_key = environ["SECRET_KEY"]
jwt_expiration_delta_seconds = int(environ["JWT_EXPIRATION_DELTA"])
debug_mode = environ["DEBUG_MODE"] in ["true", "True", "yes", "Yes", "y", "Y"]

db_uri = "postgresql://%s:%s@%s:%d/%s" % (db_user, db_password, db_host, db_port, db_resource)

