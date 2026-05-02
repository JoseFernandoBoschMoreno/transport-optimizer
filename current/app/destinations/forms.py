from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length

class DestinationForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired(), Length(max=64)])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=128)])
    lugar = StringField('Lugar', validators=[Length(max=128)])
    demanda_minima = FloatField('Demanda mínima', validators=[DataRequired()])
    submit = SubmitField('Guardar')
