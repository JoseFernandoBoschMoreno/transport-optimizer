import io
import csv
from flask import Response
from app.models import ResultHeader, ResultDetail, Origin, Destination

def export_results_to_csv(model_id, result_id):
    header = ResultHeader.query.filter_by(id=result_id, model_id=model_id).first_or_404()
    details = ResultDetail.query.filter_by(result_id=result_id).all()
    origins = {o.id: o for o in Origin.query.filter_by(model_id=model_id).all()}
    destinations = {d.id: d for d in Destination.query.filter_by(model_id=model_id).all()}

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['origin_id', 'origin', 'destination_id', 'destination', 'cantidad'])

    for d in details:
        writer.writerow([
            d.origin_id,
            origins[d.origin_id].nombre,
            d.destination_id,
            destinations[d.destination_id].nombre,
            d.cantidad
        ])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename=results_model_{model_id}_result_{result_id}.csv'
    return response
