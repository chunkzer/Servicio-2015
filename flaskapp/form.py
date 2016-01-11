from flask_wtf import Form
from wtforms.fields.html5 import EmailField
from wtforms import IntegerField, StringField, TextField,\
    PasswordField, validators, SelectMultipleField, widgets,SubmitField

class LoginForm(Form):
    email = EmailField('email', [validators.DataRequired(message=u"Introducir correo")])
    password = PasswordField('Password', [validators.DataRequired(message=u"Introducir contrasena")])

class SignUpForm(Form):
    nombre = StringField('nombre', [validators.DataRequired(message=u"Introducir nombre")])
    correo = EmailField('correo', [validators.DataRequired(message=u"Introducir correo"),\
                                    validators.Email()])
    curp = StringField('curp', [validators.DataRequired(message=u"Introducir curp")])
    escuela = StringField('escuela', [validators.DataRequired(message=u"Introducir escuela")])
    ciudad = StringField('ciudad', [validators.DataRequired(message=u"Introducir ciudad")])
    edad = IntegerField('edad', [validators.DataRequired(message=u"Introducir edad")])
    concursos = SelectMultipleField(choices=[('Matematicas', 'Matematicas'),\
            ('Fisica', 'Fisica'), ('Pre-selectivo de fisica', 'Pre-selectivo de fisica')],\
                option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    password = PasswordField('password', [validators.DataRequired(message=u"Introducir contrasena")])
    submit = SubmitField('registro')
