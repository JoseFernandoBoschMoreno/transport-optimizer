import io
import pandas as pd
from flask import send_file
from app.models import ResultHeader, ResultDetail, Origin, Destination

def export_results_to_excel(model_id, result_id):
    header = ResultHeader.query.filter_by(id=result_id, model_id=model_id).first_or_404()
    details = ResultDetail.query.filter_by(result_id=result_id).all()
    origins = {o.id: o for o in Origin.query.filter_by(model_id=model_id).all()}
    destinations = {d.id: d for d in Destination.query.filter_by(model_id=model_id).all()}

    rows = []
    for d in details:
        rows.append({
            'origin_id': d.origin_id,
            'origin': origins[d.origin_id].nombre,
            'destination_id': d.destination_id,
            'destination': destinations[d.destination_id].nombre,
            'cantidad': d.cantidad,
        })

    df = pd.DataFrame(rows)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='results')

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name=f'results_model_{model_id}_result_{result_id}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
