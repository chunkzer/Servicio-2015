from flask import url_for, redirect, flash, Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import BaseConfig
from form import LoginForm, SignUpForm
from flask.ext.login import LoginManager, login_user, \
    login_required, logout_user, current_user
from flask.ext.mail import Mail, Message
from werkzeug import secure_filename
import os, datetime
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import shutil
from collections import OrderedDict

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
    status = False
    if user.status == 'Listo':
        status = True
    files = {'Acta':user.acta, 'Credencial':user.cred, 'Foto':user.foto}
    files_status = {'acta':user.status_acta, 'cred':user.status_credencial, 'foto':user.status_foto}
    # return str(files2)
    return render_template('docs.html', file_uploaded=success, datos=files, status=status, files_status=files_status)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in BaseConfig.ALLOWED_EXTENSIONS

@app.route('/order', methods=['POST'])
def order():
    engine = create_engine("sqlite:///"+os.path.abspath(os.path.dirname(__file__))+"/app.db")
    if "criteria" in request.json:
        with engine.connect() as connection:
            query = engine.execute("select * from users where admin=0 order by status = '"+request.json["criteria"]+"' desc, date(fecha)").fetchall()
        users = {"users": [list(user) for user in query]}
        users["users"]
        return jsonify(users)
    elif "nombre" in request.json:
        with engine.connect() as connection:
            query = engine.execute("select * from users where name='"+request.json["nombre"]+"'").fetchall()
        users = {"users": [list(user) for user in query]}
        return jsonify(users)

@app.route('/files', methods=['POST'])
@login_required
def files():
    # si el usuario es administrador redirecciona (un admin no podra entrar a
    # sitios de un usuario comun)
    if request.method == 'POST':
        if current_user.admin == 1:
            return redirect(url_for('admin'))
        file_uploaded = False
        engine = create_engine("sqlite:///"+os.path.abspath(os.path.dirname(__file__))+"/app.db")
        user = current_user
        folder = BaseConfig.UPLOAD_FOLDER + "/" + user.email
        # Recorro sobre los archivos subidos
        if len(request.files.items()):
            for key, archivo in request.files.items():
                filename = secure_filename(archivo.filename)
                if filename != '' and allowed_file(filename):
                    with engine.connect() as connection:
                        a = engine.execute("select "+key+" from users where email='"+user.email+"'")
                        row = a.fetchone()
                        # Si ya habia subido archivo lo reemplazara
                        if row[key] != '':
                            os.remove(folder+"/"+row[key].split('/')[2])

                    with engine.connect() as connection:
                        engine.execute("update users set "+key+"='"+'static/'+\
                        user.email+'/'+filename+"' where email='"+user.email+"'")

                    file_path = os.path.join(folder, filename)
                    archivo.save(file_path)
                    file_uploaded = True
            if file_uploaded:
                with engine.connect() as connection:
                    a = engine.execute("select acta, cred, foto from users where email='"+user.email+"'")
                    row = a.fetchone()
                if row[0] != '' and row[1] != '' and row[2] != '':
                    query = "update users set status='Espera' where email='"+user.email+"'"
                else:
                    query = "update users set status='Enviando' where email='"+user.email+"'"

                with engine.connect() as connection:
                    engine.execute(query)


    return redirect(url_for('inicio', success=file_uploaded))

@app.route('/registro', methods=['POST'])
def registro():
    sign_form = SignUpForm(prefix="sign_form")
    log_form = LoginForm()
    if sign_form.validate_on_submit() and request.method == 'POST':
        if User.query.filter_by(email=sign_form.correo.data).first():
            return "<script type=\"text/javascript\">\
                    alert(\"El correo que introdujiste ya esta en uso. Utiliza otro correo para continuar.\");\
                    window.location.href = '/flaskapp'\
                    </script>"
        u = User()
        u.name = sign_form.nombre.data
        u.email = sign_form.correo.data
        u.curp = sign_form.curp.data
        u.edad = sign_form.edad.data
        u.escuela = sign_form.escuela.data
        u.ciudad = sign_form.ciudad.data
        u.concursos = ", ".join(sign_form.concursos.data)
        u.password = sign_form.password.data
        u.admin = 0
        u.status = 'Registrado'
        u.fecha = datetime.datetime.now()
        folder = BaseConfig.UPLOAD_FOLDER + "/" + u.email
        if os.path.exists(folder):
            shutil.rmtree(folder)

        os.mkdir(folder)
        os.chmod(folder, 0o777)
        db.session.add(u)
        db.session.commit()
        mensaje = "Haz quedado registrado en el portal del concurso\
regional de fisica y matematicas UNISON<br>Inicia sesion en\
el portal para empezar a subir los archivos necesarios.\
Una vez que hayas subido todos tus documentos el comite\
organizador se encargara de revisarlos y aprobarlos. En caso\
de que todo este correcto, recibiras un correo en el transcurso\
de unos dias indicando que haz quedado inscrito al concurso.\
<br><br>Tus datos de ingreso al portal son:<br><b>Correo:</b>\
%s<br><b>Contrasena:</b> %s" % (u.email, sign_form.password.data)
        msg = Message("Registro concurso regional de fisica y matematicas", sender = "geratarra@gmail.com", recipients=[u.email])
        msg.html = mensaje
        # mail.send(msg)
        return "<script type=\"text/javascript\">\
                alert(\"Registro exitoso. Se han enviado tus datos al correo que proporsionaste en el registro.\");\
                window.location.href = '/flaskapp'\
                </script>"
    return render_template('index.html', form_login=log_form, sign_form=sign_form)

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    if current_user.admin != 1:
        return redirect(url_for('index'))
    users = User.query.filter_by(admin=0).all()
    return render_template('lista.html', usuarios=users, admin=1)

@app.route('/datos/<estudiante>', methods=['GET'])
@login_required
def datos(estudiante):
    if current_user.admin != 1:
        return redirect(url_for('index'))
    user = User.query.filter_by(email=estudiante).first()
    return render_template('estudiante.html', user=user, admin=1)

@app.route('/calificar/<estudiante>', methods=['post'])
@login_required
def calificar(estudiante):
    if current_user.admin != 1:
        return redirect(url_for('index'))
    if len(request.form.items()) == 0:
        return "<script type=\"text/javascript\">\
                window.location.href = '/flaskapp/admin'\
                </script>"

    u = User.query.filter_by(email=estudiante).first()
    revisados = []
    rechazados = []
    aceptados = []
    engine = create_engine("sqlite:///"+os.path.abspath(os.path.dirname(__file__))+"/app.db")
    folder = BaseConfig.UPLOAD_FOLDER + "/" + u.email

    for item in request.form.items():
        doc = item[0].split('_')[1]
        revisados.append(doc.title())
        if item[1] == "1":
            aceptados.append(doc)
            with engine.connect() as connection:
                engine.execute("update users set status_"+doc+"=1 where email ='"+u.email+"'")
        else:
            rechazados.append(doc)
            with engine.connect() as connection:
                engine.execute("update users set status_"+doc+"=3 where email ='"+u.email+"'")
                a = engine.execute("select "+doc[:4]+" from users where email='"+u.email+"'")
                row = a.fetchone()
                if row[0] != '':
                    os.remove(folder+"/"+row[0].split('/')[2])
                engine.execute("update users set "+doc[:4]+"='' where email ='"+u.email+"'")

    row = engine.execute("select status_acta, status_credencial, status_foto from users where email='"+u.email+"'")
    estados = tuple(row.fetchone())
    # return "<script type=\"text/javascript\">\
    #         alert(\""+str(estados)+"\");\
    #         window.location.href = '/flaskapp/admin'\
    #         </script>"

    if len(revisados) != 0:
        mensaje = "Estimado estudiante, el comite reviso tus documentos:\
"+", ".join(revisados)+" y estas fueron las observaciones:<br>Documentos aceptados: "+", ".join(aceptados)+"\
<br>Documentos rechazados: "+", ".join(rechazados)+"<br>"
        with engine.connect() as connection:
            engine.execute("update users set revisor='"+current_user.email+"' where email ='"+u.email+"'")



    if 0 in estados or 3 in estados:
        with engine.connect() as connection:
            engine.execute("update users set status='Revisado' where email ='"+u.email+"'")
        mensaje = mensaje + "Aun tienes documentos pendientes por enviar o rechazados.\
Sube tus documentos para que no te quedes fuera!"
    else:
        with engine.connect() as connection:
            engine.execute("update users set status='Listo' where email ='"+u.email+"'")
        mensaje = mensaje + "Haz completado el registro al concurso, exito!!"

    # if len(revisados) == 3:
    #     if len(aceptados) != 3:
    #         string_aceptados = ", ".join(aceptados)
    #         string_rechazados = ", ".join(rechazados)
    #         mensaje = "Estimado estudiante, el comite reviso tus documentos y estas\
    #         fueron las observaciones:<br>Documentos aceptados: "+", ".join(aceptados)+"\
    #         <br>Documentos rechazados: "+", ".join(rechazados)+"<br>Vuelve a subir tus\
    #         documentos rechazados de manera correcta para poder revisarlos de nuevo."
    # else:
    #     if len(revisados) == 2:
    #         if len(aceptados) == 2 and 0 in estados:
    #             mensaje = "Estimado estudiante, tus documentos: "+", ".join(aceptados)+", \
    #             fueron aceptados. Sin embargo aun tienes un documento pendiente por enviar.\
    #             Envialo antes de la fecha limite para que no te quedes fuera!"
    #         elif len(aceptados) == 2 and 3 in estados:
    #             mensaje = "Estimado estudiante, el comite reviso tus documentos y estas\
    #             fueron las observaciones:<br>Documentos aceptados: "+", ".join(aceptados)+"\
    #             <br>Sin embargo, aun tienes un documento que no fue aceptado.<br>Vuelve a subir tus\
    #             documentos rechazados de manera correcta para poder revisarlos de nuevo. No te quedes fuera!"
    #         elif len(aceptados) != 2:
    #             mensaje = "Estimado estudiante, el comite reviso tus documentos:<br>\
    #             "+", ".join(revizados)+"<br>Estas fueron las observaciones:<br>\
    #             Documentos aceptados:<br>"+", ".join(aceptados)+"<br>Documentos rechazados:<br>\
    #             "+", ".join(rechazados)+"<br>Vuelve a subir tus documentos rechazados\
    #              de manera correcta para poder revisarlos de nuevo."
    #             if 0 in estados:
    #                 mensaje = mensaje+" Ademas te recordamos que tienes un documento pendiente por\
    #                  enviar. No te quedes fuera!"
    #     else:
    #         if len(aceptados) == 1:
    #             mensaje = "Estimado estudiante, tu documento: "+aceptados[0]+", fue aceptado."
    #             if 0 in estados or 3 in estados:
    #                 mensaje = mensaje+"<br>Te recordamos que aun tienes documentos pendientes por enviar\
    #                 o rechazados. Sube tus documentos para que no te quedes fuera!"
    #             else:
    #                 mensaje = mensaje+"<br>Completaste tu registro al concurso. Exito!"
    #         else:
    #             if 0 in estados:
    #                 mensaje = "Estimado estudiante, tu documento: "+rechazados[0]+", fue rechazado.\
    #                 Envialo de nuevo para que sea revisado. Ademas, te recordamos que aun tienes\
    #                  documentos pendientes por enviar. No te quedes fuera!"

    msg = Message("Registro concurso regional de fisica y matematicas", sender = "melifelix.mfn@gmail.com", recipients=[u.email, current_user.email])
    msg.html = mensaje
    # mail.send(msg)

    return "<script type=\"text/javascript\">\
            alert(\""+mensaje+". Datos revisados. El alumno recibira un correo con las observaciones.\");\
            window.location.href = '/flaskapp/admin'\
            </script>"

    return "<script type=\"text/javascript\">\
            alert(\"Datos revisados. El alumno recibira un correo con las observaciones.\");\
            window.location.href = '/flaskapp/admin'\
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
        # flash("Correo o contrasena invalido", category='error')
        return "<script type=\"text/javascript\">\
                alert(\"Correo o contrasena invalido.\");\
                window.location.href = '/flaskapp#iniciar'\
                </script>"
    return render_template('index.html', form_login=form_login, sign_form=sign_form)

if __name__ == '__main__':
    manager.run()
