from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models_bp import bp
from app import db
from app.models import TransportModel
from app.models_bp.forms import TransportModelForm

@bp.route('/')
@login_required
def index():
    models = TransportModel.query.filter_by(user_id=current_user.id).all()
    return render_template('models/index.html', models=models)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TransportModelForm()
    if form.validate_on_submit():
        model = TransportModel(
            user_id=current_user.id,
            nombre=form.nombre.data,
            descripcion=form.descripcion.data
        )
        db.session.add(model)
        db.session.commit()
        flash('Modelo creado.', 'success')
        return redirect(url_for('models_bp.index'))
    return render_template('models/form.html', form=form)

@bp.route('/<int:model_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(model_id):
    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first_or_404()
    form = TransportModelForm(obj=model)
    if form.validate_on_submit():
        model.nombre = form.nombre.data
        model.descripcion = form.descripcion.data
        db.session.commit()
        flash('Modelo actualizado.', 'success')
        return redirect(url_for('models_bp.index'))
    return render_template('models/form.html', form=form)

@bp.route('/<int:model_id>/delete', methods=['POST'])
@login_required
def delete(model_id):
    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first_or_404()
    db.session.delete(model)
    db.session.commit()
    flash('Modelo eliminado.', 'success')
    return redirect(url_for('models_bp.index'))
