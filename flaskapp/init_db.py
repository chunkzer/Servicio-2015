from __init__ import db
from models import User
import sys, shutil
from config import BaseConfig
import os
import datetime

try:
    print "Creando tabla.."
    db.drop_all()
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
    u.fecha = datetime.datetime.now()
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
    u.admin = 0
    u.status = 'Enviando'
    print "Carpeta creada"
    os.mkdir(folder)
    os.chmod(folder, 0o777)
    db.session.add(u)
    db.session.commit()
    print "Commit hecho\n\n"

    # Creo usuario del comite
    print "Creando usuario para el comite.."
    c = User()
    c.name = "Jose"
    c.curp = "NOTENGOCURP"
    c.escuela = "MIT"
    c.email = "jose@gmail.com"
    c.password = "123"
    c.ciudad = "Hermosillo"
    c.concursos = "mat"
    c.edad = 30
    print "Nombre >> ", c.name, "\nCorreo >> ", c.email
    print "Password >> 123"
    if u.verify_password("hola"):
        print "Password hashed correctly!"
    else:
        print "No se hashear la contrasena"
    print "Curp >> ", c.curp, "\nEscuela >> ", c.escuela, "\nCiudad >> ", c.ciudad
    print "Concursos >> ", c.concursos
    c.admin = 1
    db.session.add(c)
    db.session.commit()
    print "Commit hecho"
except Exception as e:
    print "Error >> ", e
