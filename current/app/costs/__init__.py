from flask import Blueprint

bp = Blueprint('costs', __name__, template_folder='../templates')

from app.costs import routes  # noqa
