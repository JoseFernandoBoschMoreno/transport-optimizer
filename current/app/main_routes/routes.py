from flask import render_template
from flask_login import login_required, current_user
from app.main_routes import bp

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
