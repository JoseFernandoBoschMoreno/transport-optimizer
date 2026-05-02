from ortools.linear_solver import pywraplp
from flask import current_app
from app import db
from app.models import Origin, Destination, Cost

def solve_transport_model(model_id):
    origins = Origin.query.filter_by(model_id=model_id).all()
    destinations = Destination.query.filter_by(model_id=model_id).all()
    costs = Cost.query.filter_by(model_id=model_id).all()

    if not origins or not destinations or not costs:
        return {'feasible': False, 'status': 'NO_DATA', 'flows': {}, 'total_cost': 0.0}

    use_gurobi = current_app.config.get('USE_GUROBI', False)
    if use_gurobi:
        try:
            import gurobipy as gp  # noqa
            solver = pywraplp.Solver.CreateSolver('GUROBI')
        except Exception:
            solver = pywraplp.Solver.CreateSolver('SCIP')
    else:
        solver = pywraplp.Solver.CreateSolver('SCIP')

    if solver is None:
        return {'feasible': False, 'status': 'NO_SOLVER', 'flows': {}, 'total_cost': 0.0}

    origin_ids = [o.id for o in origins]
    dest_ids = [d.id for d in destinations]

    cost_dict = {}
    for c in costs:
        cost_dict[(c.origin_id, c.destination_id)] = c.costo

    x = {}
    for o_id in origin_ids:
        for d_id in dest_ids:
            if (o_id, d_id) in cost_dict:
                x[(o_id, d_id)] = solver.NumVar(0, solver.infinity(), f'x_{o_id}_{d_id}')

    # Supply constraints
    for o in origins:
        solver.Add(
            sum(x[(o.id, d.id)] for d in destinations if (o.id, d.id) in x) <= o.capacidad_maxima
        )

    # Demand constraints
    for d in destinations:
        solver.Add(
            sum(x[(o.id, d.id)] for o in origins if (o.id, d.id) in x) >= d.demanda_minima
        )

    objective = solver.Objective()
    for (o_id, d_id), var in x.items():
        objective.SetCoefficient(var, cost_dict[(o_id, d_id)])
    objective.SetMinimization()

    status = solver.Solve()

    if status not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        return {'feasible': False, 'status': 'INFEASIBLE', 'flows': {}, 'total_cost': 0.0}

    flows = {}
    total_cost = 0.0
    for key, var in x.items():
        val = var.solution_value()
        if val > 1e-6:
            flows[key] = val
            total_cost += val * cost_dict[key]

    return {
        'feasible': True,
        'status': 'OPTIMAL' if status == pywraplp.Solver.OPTIMAL else 'FEASIBLE',
        'flows': flows,
        'total_cost': total_cost,
    }
