from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired

class CostForm(FlaskForm):
    origin_id = SelectField('Origen', coerce=int, validators=[DataRequired()])
    destination_id = SelectField('Destino', coerce=int, validators=[DataRequired()])
    costo = FloatField('Costo unitario', validators=[DataRequired()])
    submit = SubmitField('Guardar')
