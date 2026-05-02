from flask import Blueprint

bp = Blueprint('origins', __name__, template_folder='../templates')

from app.origins import routes  # noqa
