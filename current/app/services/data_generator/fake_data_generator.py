import random
from flask import flash
from app import db
from app.models import Origin, Destination, Cost, TransportModel

def generate_fake_model(current_user, num_origins=3, num_destinations=3):
    model = TransportModel(
        user_id=current_user.id,
        nombre='Modelo ficticio',
        descripcion='Modelo generado automáticamente para pruebas.'
    )
    db.session.add(model)
    db.session.flush()

    generate_fake_data_for_model(model.id, num_origins, num_destinations)
    db.session.commit()
    flash('Modelo ficticio generado.', 'success')
    return model.id

def generate_fake_data_for_model(model_id, num_origins=3, num_destinations=3):
    origins = []
    destinations = []

    total_demand = 0
    for i in range(num_origins):
        cap = random.randint(50, 150)
        o = Origin(
            codigo=f'O{i+1}',
            nombre=f'Origen {i+1}',
            lugar=f'Ciudad O{i+1}',
            capacidad_maxima=cap,
            model_id=model_id
        )
        db.session.add(o)
        db.session.flush()
        origins.append(o)

    for j in range(num_destinations):
        dem = random.randint(30, 80)
        total_demand += dem
        d = Destination(
            codigo=f'D{j+1}',
            nombre=f'Destino {j+1}',
            lugar=f'Ciudad D{j+1}',
            demanda_minima=dem,
            model_id=model_id
        )
        db.session.add(d)
        db.session.flush()
        destinations.append(d)

    # Ajustar capacidades para garantizar factibilidad
    total_capacity = sum(o.capacidad_maxima for o in origins)
    if total_capacity < total_demand:
        factor = (total_demand / total_capacity) + 0.2
        for o in origins:
            o.capacidad_maxima *= factor

    for o in origins:
        for d in destinations:
            c = Cost(
                origin_id=o.id,
                destination_id=d.id,
                costo=random.randint(5, 20),
                model_id=model_id
            )
            db.session.add(c)
