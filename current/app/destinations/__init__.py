from flask import Blueprint

bp = Blueprint('destinations', __name__, template_folder='../templates')

from app.destinations import routes  # noqa
