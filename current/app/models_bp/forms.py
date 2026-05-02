from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class TransportModelForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=128)])
    descripcion = TextAreaField('Descripción')
    submit = SubmitField('Guardar')
