import db_password

PORT = 5000
DEBUG = True
DB_CONFIG = "mysql://%s:%s@%s/%s" \
    % (db_password.USER, db_password.PASSWD, \
       db_password.SERVER, db_password.DB)
