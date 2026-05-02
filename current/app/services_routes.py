from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import TransportModel
from app.services.importer.excel_importer import import_from_excel
from app.services.importer.csv_importer import import_from_csv
from app.services.importer.json_importer import import_from_json
from app.services.data_generator.fake_data_generator import generate_fake_model, generate_fake_data_for_model

bp_services = Blueprint('services_bp', __name__, template_folder='templates')

def user_owns_model(model_id):
    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first()
    return model is not None

@bp_services.route('/import/<int:model_id>/', methods=['GET', 'POST'])
@login_required
def import_data(model_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))

    if request.method == 'POST':
        file = request.files.get('file')
        fmt = request.form.get('format')
        entity = request.form.get('entity')

        if not file:
            flash('Debe seleccionar un archivo.', 'danger')
            return redirect(request.url)

        if fmt == 'excel':
            import_from_excel(file, model_id, current_user)
        elif fmt == 'csv':
            import_from_csv(file, model_id, current_user, entity)
        elif fmt == 'json':
            import_from_json(file, model_id, current_user)
        else:
            flash('Formato no soportado.', 'danger')

        return redirect(url_for('models_bp.index'))

    return render_template('services/import.html', model_id=model_id)

@bp_services.route('/generate_fake_model', methods=['POST'])
@login_required
def generate_model():
    model_id = generate_fake_model(current_user)
    return redirect(url_for('models_bp.edit', model_id=model_id))

@bp_services.route('/generate_fake_data/<int:model_id>', methods=['POST'])
@login_required
def generate_data(model_id):
    if not user_owns_model(model_id):
        flash('No tiene acceso a este modelo.', 'danger')
        return redirect(url_for('models_bp.index'))
    generate_fake_data_for_model(model_id)
    flash('Datos ficticios generados.', 'success')
    return redirect(url_for('models_bp.edit', model_id=model_id))
