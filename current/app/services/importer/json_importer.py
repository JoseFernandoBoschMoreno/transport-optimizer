import json
from flask import flash
from app import db
from app.models import Origin, Destination, Cost, TransportModel

def import_from_json(file_storage, model_id, current_user):
    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first()
    if not model:
        flash('No tiene acceso a este modelo.', 'danger')
        return False

    try:
        data = json.load(file_storage)

        for row in data.get('origins', []):
            origin = Origin(
                codigo=str(row['codigo']),
                nombre=str(row['nombre']),
                lugar=str(row.get('lugar', '')),
                capacidad_maxima=float(row['capacidad_maxima']),
                model_id=model_id
            )
            db.session.add(origin)

        for row in data.get('destinations', []):
            dest = Destination(
                codigo=str(row['codigo']),
                nombre=str(row['nombre']),
                lugar=str(row.get('lugar', '')),
                demanda_minima=float(row['demanda_minima']),
                model_id=model_id
            )
            db.session.add(dest)

        for row in data.get('costs', []):
            cost = Cost(
                origin_id=int(row['origin_id']),
                destination_id=int(row['destination_id']),
                costo=float(row['costo']),
                model_id=model_id
            )
            db.session.add(cost)

        db.session.commit()
        flash('Datos importados desde JSON.', 'success')
        return True
    except Exception as e:
        db.session.rollback()
        flash(f'Error al importar JSON: {e}', 'danger')
        return False
