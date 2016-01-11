import os


# default config

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    UPLOAD_FOLDER = os.getcwd() + "/static"
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # MAIL_DEBUG : default app.debug
    MAIL_USERNAME = "geratarra@gmail.com"
    MAIL_PASSWORD = "3s28mfdt"
    # DEFAULT_MAIL_SENDER : default None
    SECRET_KEY = '5\x02\xc4\x14\xdcM\xc1\xda\xf69\xa8\ \
                  xbbS\xec\x8a\x061{\x16\xed&S\xc5/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'app.db')
