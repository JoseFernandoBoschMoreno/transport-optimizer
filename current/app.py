from app import create_app, db
from flask_migrate import Migrate
from app.models import User, TransportModel, Origin, Destination, Cost, ResultHeader, ResultDetail
from app.services_routes import bp_services

app = create_app()
migrate = Migrate(app, db)

app.register_blueprint(bp_services, url_prefix='/services')

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'TransportModel': TransportModel,
        'Origin': Origin,
        'Destination': Destination,
        'Cost': Cost,
        'ResultHeader': ResultHeader,
        'ResultDetail': ResultDetail,
    }

if __name__ == '__main__':
    app.run(debug=True)
