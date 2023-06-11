import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Contiene tutte le configurazioni dell'applicazione.
    Da questa classe ereditano le classi di Development,
    Production e Testing. A seconda di cosa si vuole fare,
    basterà scegliere la classe da `__init__.py`.
    """
    # Config Variables
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SESSION_COOKIE_SECURE = True
    TEMPLATES_FOLDER = 'templates'

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Config):
    pass


class Development(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_ECHO = True


class Testing(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
