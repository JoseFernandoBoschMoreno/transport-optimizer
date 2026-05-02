import io
import pandas as pd
from flask import flash
from app import db
from app.models import Origin, Destination, Cost, TransportModel

def import_from_excel(file_storage, model_id, current_user):
    model = TransportModel.query.filter_by(id=model_id, user_id=current_user.id).first()
    if not model:
        flash('No tiene acceso a este modelo.', 'danger')
        return False

    try:
        data = file_storage.read()
        excel_file = io.BytesIO(data)
        xls = pd.ExcelFile(excel_file)

        if 'origins' in xls.sheet_names:
            df_o = pd.read_excel(xls, 'origins')
            for _, row in df_o.iterrows():
                origin = Origin(
                    codigo=str(row['codigo']),
                    nombre=str(row['nombre']),
                    lugar=str(row.get('lugar', '')),
                    capacidad_maxima=float(row['capacidad_maxima']),
                    model_id=model_id
                )
                db.session.add(origin)

        if 'destinations' in xls.sheet_names:
            df_d = pd.read_excel(xls, 'destinations')
            for _, row in df_d.iterrows():
                dest = Destination(
                    codigo=str(row['codigo']),
                    nombre=str(row['nombre']),
                    lugar=str(row.get('lugar', '')),
                    demanda_minima=float(row['demanda_minima']),
                    model_id=model_id
                )
                db.session.add(dest)

        if 'costs' in xls.sheet_names:
            df_c = pd.read_excel(xls, 'costs')
            for _, row in df_c.iterrows():
                cost = Cost(
                    origin_id=int(row['origin_id']),
                    destination_id=int(row['destination_id']),
                    costo=float(row['costo']),
                    model_id=model_id
                )
                db.session.add(cost)

        db.session.commit()
        flash('Datos importados desde Excel.', 'success')
        return True
    except Exception as e:
        db.session.rollback()
        flash(f'Error al importar Excel: {e}', 'danger')
        return False
