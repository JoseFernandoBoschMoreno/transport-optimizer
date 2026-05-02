from flask import jsonify
from app.models import ResultHeader, ResultDetail, Origin, Destination

def export_results_to_json(model_id, result_id):
    header = ResultHeader.query.filter_by(id=result_id, model_id=model_id).first_or_404()
    details = ResultDetail.query.filter_by(result_id=result_id).all()
    origins = {o.id: o for o in Origin.query.filter_by(model_id=model_id).all()}
    destinations = {d.id: d for d in Destination.query.filter_by(model_id=model_id).all()}

    data = {
        'model_id': model_id,
        'result_id': result_id,
        'costo_total': header.costo_total,
        'estado': header.estado,
        'details': []
    }

    for d in details:
        data['details'].append({
            'origin_id': d.origin_id,
            'origin': origins[d.origin_id].nombre,
            'destination_id': d.destination_id,
            'destination': destinations[d.destination_id].nombre,
            'cantidad': d.cantidad
        })

    return jsonify(data)
