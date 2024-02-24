from rq import Queue
from redis import Redis
from .modelos import db, Entrenamiento
from datetime import datetime
from flask import request
from microservicio_monitor import create_app

q = Queue(connection=Redis(host='localhost', port=6379, db=0))

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


def send_entrenamiento(entrenamiento_data):
    entrenamiento = Entrenamiento(
        id=entrenamiento_data['id'],
        fecha=datetime.strptime(entrenamiento_data['fecha'], '%y-%m-%d %H:%M:%S'),
        distancia=entrenamiento_data['distancia'],
        tiempo=entrenamiento_data['tiempo'],
        calorias=entrenamiento_data['calorias'],
        usuario_id=entrenamiento_data['usuario_id'])
    print("Sincronizado " + entrenamiento)
    db.session.add(entrenamiento)
    db.session.commit()