from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Entrenamiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    distancia = db.Column(db.Float)
    tiempo = db.Column(db.Float)
    calorias = db.Column(db.Float)
    usuario_id = db.Column(db.Integer)
