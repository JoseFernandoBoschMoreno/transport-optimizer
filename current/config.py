import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'transport.db')
    else:
        # Convertir rutas relativas en absolutas
        if SQLALCHEMY_DATABASE_URI.startswith("sqlite:///") and not SQLALCHEMY_DATABASE_URI.startswith("sqlite:////"):
            relative_path = SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
            absolute_path = os.path.join(basedir, relative_path)
            SQLALCHEMY_DATABASE_URI = "sqlite:///" + absolute_path

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_GUROBI = os.environ.get('USE_GUROBI', 'False').lower() == 'true'