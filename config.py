import password

PORT = 5000
DEBUG = True
DB_CONFIG = "mysql://%s:%s@%s/%s?charset=utf8" \
    % (password.USER, password.PASSWD, \
       password.SERVER, password.DB)
