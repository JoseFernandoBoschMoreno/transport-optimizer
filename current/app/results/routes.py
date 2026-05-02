from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.results import bp
from app import db
from app.models import (
    TransportModel,
    ResultHeader,
    ResultDetail,
    Origin,
    Destination,
)
from app.services.optimization.transport_model import solve_transport_model
from app.services.exporter.excel_exporter import export_results_to_excel
from app.services.exporter.csv_exporter import export_results_to_csv
from app.services.exporter.json_exporter import export_results_to_json

def user_owns_model(model_id):
    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first()
    return model is not None

@bp.route('/<int:model_id>/')
@login_required
def index(model_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    headers = ResultHeader.query.filter_by(model_id=model_id).all()
    return render_template('results/index.html', headers=headers, model_id=model_id)

@bp.route('/<int:model_id>/run', methods=['POST'])
@login_required
def run(model_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))

    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first_or_404()
    solution = solve_transport_model(model_id)

    if not solution['feasible']:
        flash('Modelo infactible o error en la optimización.', 'danger')
        return redirect(url_for('results.index', model_id=model_id))

    header = ResultHeader(
        model_id=model_id,
        costo_total=solution['total_cost'],
        estado=solution['status']
    )
    db.session.add(header)
    db.session.flush()

    for (o_id, d_id), qty in solution['flows'].items():
        detail = ResultDetail(
            result_id=header.id,
            origin_id=o_id,
            destination_id=d_id,
            cantidad=qty
        )
        db.session.add(detail)

    db.session.commit()
    flash('Optimización ejecutada.', 'success')
    return redirect(url_for('results.view', model_id=model_id, result_id=header.id))

@bp.route('/<int:model_id>/<int:result_id>/view')
@login_required
def view(model_id, result_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    header = ResultHeader.query.filter_by(id=result_id, model_id=model_id).first_or_404()
    details = ResultDetail.query.filter_by(result_id=result_id).all()
    origins = {o.id: o for o in Origin.query.filter_by(model_id=model_id).all()}
    destinations = {d.id: d for d in Destination.query.filter_by(model_id=model_id).all()}
    return render_template(
        'results/view.html',
        header=header,
        details=details,
        origins=origins,
        destinations=destinations,
        model_id=model_id
    )

@bp.route('/<int:model_id>/<int:result_id>/export/excel')
@login_required
def export_excel(model_id, result_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    return export_results_to_excel(model_id, result_id)

@bp.route('/<int:model_id>/<int:result_id>/export/csv')
@login_required
def export_csv(model_id, result_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    return export_results_to_csv(model_id, result_id)

@bp.route('/<int:model_id>/<int:result_id>/export/json')
@login_required
def export_json(model_id, result_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    return export_results_to_json(model_id, result_id)
