from flask import url_for, redirect, flash, Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import BaseConfig
from form import LoginForm, SignUpForm
from flask.ext.login import LoginManager, login_user, \
    login_required, logout_user, current_user
from flask.ext.mail import Mail, Message
from werkzeug import secure_filename
import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import shutil

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

# Import database models with app context
with app.app_context():
    from models import *

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(401)
def unau(e):
    return "Acceso no autorizado, favor de iniciar sesion.", 401

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(unicode(user_id))

@app.route('/inicio/<success>')
@login_required
def inicio(success):
    user = current_user
    files = {'Acta':user.acta, 'Credencial':user.cred, 'Foto':user.foto}
    return render_template('docs.html', file_uploaded=success, datos=files)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in BaseConfig.ALLOWED_EXTENSIONS

@app.route('/files', methods=['GET', 'POST'])
@login_required
def files():
    file_uploaded = False
    engine = create_engine("sqlite:///app.db")
    if request.method == 'POST':
        user = current_user
        folder = BaseConfig.UPLOAD_FOLDER + "/" + user.email
        for key, archivo in request.files.items():
            filename = secure_filename(archivo.filename)
            if filename != '' and allowed_file(filename):
                with engine.connect() as connection:
                    a = engine.execute("select "+key+" from users where email='"+user.email+"'")
                    row = a.fetchone()
                    if row[key] != '':
                        os.remove(row[key])

                with engine.connect() as connection:
                    engine.execute("update users set "+key+"='"+'static/'+\
                    user.email+'/'+filename+"' where email='"+user.email+"'")
                file_path = os.path.join(folder, filename)
                archivo.save(file_path)
                file_uploaded = True
    return redirect(url_for('inicio', success=file_uploaded))

@app.route('/registro', methods=['POST'])
def registro():
    sign_form = SignUpForm(prefix="sign_form")
    log_form = LoginForm()
    if sign_form.validate_on_submit() and request.method == 'POST':
        if User.query.filter_by(email=sign_form.correo.data).first():
            flash("El correo que introdujiste ya esta en uso.")
            return redirect(url_for('index'))
        u = User()
        u.name = sign_form.nombre.data
        u.email = sign_form.correo.data
        u.curp = sign_form.curp.data
        u.escuela = sign_form.escuela.data
        u.ciudad = sign_form.ciudad.data
        u.concursos = " ".join(sign_form.concursos.data)
        u.password = sign_form.password.data
        db.session.add(u)
        db.session.commit()
        folder = BaseConfig.UPLOAD_FOLDER + "/" + u.email
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
        mensaje = "Haz quedado registrado en el portal del concurso\
                    regional de fisica y matematicas UNISON<br>Inicia sesion en\
                    el portal para empezar a subir los archivos necesarios.\
                    Una vez que hayas subido todos tus documentos el comite\
                    organizador se encargara de revisarlos y aprobarlos. En caso\
                    de que todo este correcto, recibiras un correo en el transcurso\
                    de unos dias indicando que haz quedado inscrito al concurso.\
                    <br><br>Tus datos de ingreso al portal son:<br><b>Correo:</b>\
                    %s<br><b>Contrasena:</b> %s" % (u.email, sign_form.password.data)
        msg = Message("Registro concurso regional de fisica y matematicas", sender = "melifelix.mfn@gmail.com", recipients=[u.email])
        msg.html = mensaje
        mail.send(msg)
        return "<script type=\"text/javascript\">\
                alert(\"Registro exitoso. Se han enviado tus datos al correo que proporsionaste en el registro.\");\
                window.location.href = '/'\
                </script>"
    return render_template('index.html', form_login=log_form, sign_form=sign_form)

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    if current_user.admin != 1:
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('lista.html', usuarios=users, admin=1)

@app.route('/datos/<estudiante>', methods=['GET'])
@login_required
def datos(estudiante):
    if current_user.admin != 1:
        return redirect(url_for('index'))
    user = User.query.filter_by(email=estudiante).first()
    return render_template('estudiante.html', user=user, admin=1)

@app.route('/calificar/<estudiante>', methods=['post', 'get'])
@login_required
def calificar(estudiante):
    if current_user.admin != 1:
        return redirect(url_for('index'))
    u = User.query.filter_by(email=estudiante).first()
    if all(map(lambda x: True if x == '1' else False, request.form.values())):
        if len(request.form.values()) == 3:
            pass
            # mensaje = "Estimado estudiante tus documentos enviados han sido\
            #             revisados y aprobados por el comite, esto quiere decir\
            #             que completaste tu registro al concurso. Exito
            u.status = 1
            db.session.commit()
        else:
            pass
            # mensaje = "Estimado estudiante, tus documentos han sido revisados\
            #            y aprobados por el comite, sin embargo te recordamos\
            #            que aun tienes algun/os documentos pendientes por\
            #            entregar para que quedes registrado en el concurso.\
            #            Entra al portal y subes tus archivos faltantes para\
            #            que no quedes fuera."
        pass
        # msg = Message("Registro concurso regional de fisica y matematicas", sender = "concurso@uson.mx", recipients=[u.email])
        # msg.html = mensaje
        # mail.send(msg)
    else:
        pass
    return "<script type=\"text/javascript\">\
            alert(\"Datos revisados. El alumno recibira un correo con las observaciones.\");\
            window.location.href = '/admin'\
            </script>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        logout_user()
    form_login = LoginForm(prefix="form_login")
    sign_form = SignUpForm(prefix="sign_form")
    if form_login.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(email=form_login.email.data).first()
        if user is not None and user.verify_password(form_login.password.data):
            if user.admin == 1:
                login_user(user)
                return redirect(request.args.get('next') or url_for('admin'))
            login_user(user)
            return redirect(request.args.get('next') or url_for('inicio', success=False))
        flash("Correo o contrasena invalido")

    return render_template('index.html', form_login=form_login, sign_form=sign_form)

if __name__ == '__main__':
    manager.run()
