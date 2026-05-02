from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='consulta')

    models = db.relationship('TransportModel', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_analyst(self):
        return self.role == 'analista'

    def is_viewer(self):
        return self.role == 'consulta'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class TransportModel(db.Model):
    __tablename__ = 'transport_models'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nombre = db.Column(db.String(128), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    origins = db.relationship('Origin', backref='model', lazy=True, cascade='all, delete-orphan')
    destinations = db.relationship('Destination', backref='model', lazy=True, cascade='all, delete-orphan')
    costs = db.relationship('Cost', backref='model', lazy=True, cascade='all, delete-orphan')
    results = db.relationship('ResultHeader', backref='model', lazy=True, cascade='all, delete-orphan')


class Origin(db.Model):
    __tablename__ = 'origins'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(64), nullable=False)
    nombre = db.Column(db.String(128), nullable=False)
    lugar = db.Column(db.String(128))
    capacidad_maxima = db.Column(db.Float, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('transport_models.id'), nullable=False)


class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(64), nullable=False)
    nombre = db.Column(db.String(128), nullable=False)
    lugar = db.Column(db.String(128))
    demanda_minima = db.Column(db.Float, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('transport_models.id'), nullable=False)


class Cost(db.Model):
    __tablename__ = 'costs'
    id = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.Integer, db.ForeignKey('origins.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('transport_models.id'), nullable=False)


class ResultHeader(db.Model):
    __tablename__ = 'result_headers'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('transport_models.id'), nullable=False)
    costo_total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(64), nullable=False)

    details = db.relationship('ResultDetail', backref='result', lazy=True, cascade='all, delete-orphan')


class ResultDetail(db.Model):
    __tablename__ = 'result_details'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('result_headers.id'), nullable=False)
    origin_id = db.Column(db.Integer, db.ForeignKey('origins.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
