from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.users import bp
from app import db
from app.models import User
from app.users.forms import UserForm

def admin_required():
    if not current_user.is_authenticated or not current_user.is_admin():
        return False
    return True

@bp.route('/')
@login_required
def index():
    if not admin_required():
        flash('Acceso restringido a administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    users = User.query.all()
    return render_template('users/index.html', users=users)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not admin_required():
        flash('Acceso restringido a administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        if form.password.data:
            user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuario creado.', 'success')
        return redirect(url_for('users.index'))
    return render_template('users/form.html', form=form)

@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    if not admin_required():
        flash('Acceso restringido a administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Usuario actualizado.', 'success')
        return redirect(url_for('users.index'))
    return render_template('users/form.html', form=form)

@bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete(user_id):
    if not admin_required():
        flash('Acceso restringido a administradores.', 'danger')
        return redirect(url_for('main.dashboard'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado.', 'success')
    return redirect(url_for('users.index'))
