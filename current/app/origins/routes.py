from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.origins import bp
from app import db
from app.models import Origin, TransportModel
from app.origins.forms import OriginForm

def user_owns_model(model_id):
    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first()
    return model is not None

@bp.route('/<int:model_id>/')
@login_required
def index(model_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    origins = Origin.query.filter_by(model_id=model_id).all()
    return render_template('origins/index.html', origins=origins, model_id=model_id)

@bp.route('/<int:model_id>/create', methods=['GET', 'POST'])
@login_required
def create(model_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    form = OriginForm()
    if form.validate_on_submit():
        origin = Origin(
            codigo=form.codigo.data,
            nombre=form.nombre.data,
            lugar=form.lugar.data,
            capacidad_maxima=form.capacidad_maxima.data,
            model_id=model_id
        )
        db.session.add(origin)
        db.session.commit()
        flash('Origen creado.', 'success')
        return redirect(url_for('origins.index', model_id=model_id))
    return render_template('origins/form.html', form=form, model_id=model_id)

@bp.route('/<int:model_id>/<int:origin_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(model_id, origin_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    origin = Origin.query.filter_by(id=origin_id, model_id=model_id).first_or_404()
    form = OriginForm(obj=origin)
    if form.validate_on_submit():
        origin.codigo = form.codigo.data
        origin.nombre = form.nombre.data
        origin.lugar = form.lugar.data
        origin.capacidad_maxima = form.capacidad_maxima.data
        db.session.commit()
        flash('Origen actualizado.', 'success')
        return redirect(url_for('origins.index', model_id=model_id))
    return render_template('origins/form.html', form=form, model_id=model_id)

@bp.route('/<int:model_id>/<int:origin_id>/delete', methods=['POST'])
@login_required
def delete(model_id, origin_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    origin = Origin.query.filter_by(id=origin_id, model_id=model_id).first_or_404()
    db.session.delete(origin)
    db.session.commit()
    flash('Origen eliminado.', 'success')
    return redirect(url_for('origins.index', model_id=model_id))
