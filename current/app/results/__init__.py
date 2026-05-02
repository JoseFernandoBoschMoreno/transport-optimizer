from flask import Blueprint

bp = Blueprint('results', __name__, template_folder='../templates')

from app.results import routes  # noqa
