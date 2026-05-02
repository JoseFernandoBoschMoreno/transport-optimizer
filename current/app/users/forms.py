from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional

class UserForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Contraseña (dejar en blanco para no cambiar)', validators=[Optional()])
    role = SelectField('Rol', choices=[('admin', 'Administrador'), ('analista', 'Analista'), ('consulta', 'Consulta')])
    submit = SubmitField('Guardar')
