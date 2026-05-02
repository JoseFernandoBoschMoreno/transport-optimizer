from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.destinations import bp
from app import db
from app.models import Destination, TransportModel
from app.destinations.forms import DestinationForm

def user_owns_model(model_id):
    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first()
    return model is not None

@bp.route('/<int:model_id>/')
@login_required
def index(model_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    destinations = Destination.query.filter_by(model_id=model_id).all()
    return render_template('destinations/index.html', destinations=destinations, model_id=model_id)

@bp.route('/<int:model_id>/create', methods=['GET', 'POST'])
@login_required
def create(model_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    form = DestinationForm()
    if form.validate_on_submit():
        dest = Destination(
            codigo=form.codigo.data,
            nombre=form.nombre.data,
            lugar=form.lugar.data,
            demanda_minima=form.demanda_minima.data,
            model_id=model_id
        )
        db.session.add(dest)
        db.session.commit()
        flash('Destino creado.', 'success')
        return redirect(url_for('destinations.index', model_id=model_id))
    return render_template('destinations/form.html', form=form, model_id=model_id)

@bp.route('/<int:model_id>/<int:dest_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(model_id, dest_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    dest = Destination.query.filter_by(id=dest_id, model_id=model_id).first_or_404()
    form = DestinationForm(obj=dest)
    if form.validate_on_submit():
        dest.codigo = form.codigo.data
        dest.nombre = form.nombre.data
        dest.lugar = form.lugar.data
        dest.demanda_minima = form.demanda_minima.data
        db.session.commit()
        flash('Destino actualizado.', 'success')
        return redirect(url_for('destinations.index', model_id=model_id))
    return render_template('destinations/form.html', form=form, model_id=model_id)

@bp.route('/<int:model_id>/<int:dest_id>/delete', methods=['POST'])
@login_required
def delete(model_id, dest_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    dest = Destination.query.filter_by(id=dest_id, model_id=model_id).first_or_404()
    db.session.delete(dest)
    db.session.commit()
    flash('Destino eliminado.', 'success')
    return redirect(url_for('destinations.index', model_id=model_id))
