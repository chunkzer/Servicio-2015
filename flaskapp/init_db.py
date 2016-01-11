from app import db
from models import User
import sys, shutil
from config import BaseConfig
import os

try:
    print "Creando tabla.."
    db.create_all()
    db.session.commit()
    db.session.close()
    print "Tabla creada exitosamente"
except Exception as e:
    print "Error al crear la tabla y hacer commit: ", e

try:
    print "Creando usuario de prueba.."
    u = User()
    u.name = "Gerardo"
    u.curp = "TASG931201HNLRRR09"
    u.escuela = "Unison"
    u.email = "geratarra@gmail.com"
    u.password = "hola"
    u.ciudad = "Hermosillo"
    u.concursos = "mat"
    u.edad = 22
    # u.acta = u.cred = u.foto = ''
    print "Nombre >> ", u.name, "\nCorreo >> ", u.email
    print "Password >> hola"
    if u.verify_password("hola"):
        print "Password hashed correctly!"
    else:
        print "No se hashear la contrasena"
    print "Curp >> ", u.curp, "\nEscuela >> ", u.escuela, "\nCiudad >> ", u.ciudad
    print "Concursos >> ", u.concursos
    folder = BaseConfig.UPLOAD_FOLDER + "/" + u.email
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
    db.session.add(u)
    db.session.commit()
    print "Commit hecho"
except Exception as e:
    print "Error >> ", e
