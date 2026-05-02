import io
import pandas as pd
from flask import flash
from app import db
from app.models import Origin, Destination, Cost, TransportModel

def import_from_csv(file_storage, model_id, current_user, entity):
    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first()
    if not model:
        flash('No tiene acceso a este modelo.', 'danger')
        return False

    try:
        data = file_storage.read().decode('utf-8')
        csv_file = io.StringIO(data)
        df = pd.read_csv(csv_file)

        if entity == 'origins':
            for _, row in df.iterrows():
                origin = Origin(
                    codigo=str(row['codigo']),
                    nombre=str(row['nombre']),
                    lugar=str(row.get('lugar', '')),
                    capacidad_maxima=float(row['capacidad_maxima']),
                    model_id=model_id
                )
                db.session.add(origin)
        elif entity == 'destinations':
            for _, row in df.iterrows():
                dest = Destination(
                    codigo=str(row['codigo']),
                    nombre=str(row['nombre']),
                    lugar=str(row.get('lugar', '')),
                    demanda_minima=float(row['demanda_minima']),
                    model_id=model_id
                )
                db.session.add(dest)
        elif entity == 'costs':
            for _, row in df.iterrows():
                cost = Cost(
                    origin_id=int(row['origin_id']),
                    destination_id=int(row['destination_id']),
                    costo=float(row['costo']),
                    model_id=model_id
                )
                db.session.add(cost)

        db.session.commit()
        flash('Datos importados desde CSV.', 'success')
        return True
    except Exception as e:
        db.session.rollback()
        flash(f'Error al importar CSV: {e}', 'danger')
        return False
