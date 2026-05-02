from flask import Blueprint

bp = Blueprint('models_bp', __name__, template_folder='../templates')

from app.models_bp import routes  # noqa
