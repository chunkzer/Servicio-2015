from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    edad = db.Column(db.Integer)
    curp = db.Column(db.String, nullable=False)
    escuela = db.Column(db.String, nullable=False)
    ciudad = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    concursos = db.Column(db.String, nullable=False)
    acta = db.Column(db.String, default='')
    cred = db.Column(db.String, default='')
    foto = db.Column(db.String, default='')
    admin = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "Usuario >> " + self.name

"""
class Concursos(db.Model):
    __tablename__ = "Concursos"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mat = db.Column(db.Boolean)
    fisica = db.Column(db.Boolean)
    pre_fisica = db.Column(db.Boolean)
"""
