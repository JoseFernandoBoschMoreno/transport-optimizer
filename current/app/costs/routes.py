from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.costs import bp
from app import db
from app.models import Cost, TransportModel, Origin, Destination
from app.costs.forms import CostForm

def user_owns_model(model_id):
    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first()
    return model is not None

@bp.route('/<int:model_id>/')
@login_required
def index(model_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    costs = Cost.query.filter_by(model_id=model_id).all()
    return render_template('costs/index.html', costs=costs, model_id=model_id)

@bp.route('/<int:model_id>/create', methods=['GET', 'POST'])
@login_required
def create(model_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    form = CostForm()
    form.origin_id.choices = [(o.id, o.nombre) for o in Origin.query.filter_by(model_id=model_id).all()]
    form.destination_id.choices = [(d.id, d.nombre) for d in Destination.query.filter_by(model_id=model_id).all()]
    if form.validate_on_submit():
        cost = Cost(
            origin_id=form.origin_id.data,
            destination_id=form.destination_id.data,
            costo=form.costo.data,
            model_id=model_id
        )
        db.session.add(cost)
        db.session.commit()
        flash('Costo creado.', 'success')
        return redirect(url_for('costs.index', model_id=model_id))
    return render_template('costs/form.html', form=form, model_id=model_id)

@bp.route('/<int:model_id>/<int:cost_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(model_id, cost_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    cost = Cost.query.filter_by(id=cost_id, model_id=model_id).first_or_404()
    form = CostForm(obj=cost)
    form.origin_id.choices = [(o.id, o.nombre) for o in Origin.query.filter_by(model_id=model_id).all()]
    form.destination_id.choices = [(d.id, d.nombre) for d in Destination.query.filter_by(model_id=model_id).all()]
    if form.validate_on_submit():
        cost.origin_id = form.origin_id.data
        cost.destination_id = form.destination_id.data
        cost.costo = form.costo.data
        db.session.commit()
        flash('Costo actualizado.', 'success')
        return redirect(url_for('costs.index', model_id=model_id))
    return render_template('costs/form.html', form=form, model_id=model_id)

@bp.route('/<int:model_id>/<int:cost_id>/delete', methods=['POST'])
@login_required
def delete(model_id, cost_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    cost = Cost.query.filter_by(id=cost_id, model_id=model_id).first_or_404()
    db.session.delete(cost)
    db.session.commit()
    flash('Costo eliminado.', 'success')
    return redirect(url_for('costs.index', model_id=model_id))
