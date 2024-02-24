from rq import Queue
from redis import Redis
from .modelos import db, Entrenamiento, EntrenamientoSchema

q = Queue(connection=Redis(host='localhost', port=6379, db=0))

def send_entrenamiento(entrenamiento_data):
    entrenamiento = Entrenamiento(
        id=entrenamiento_data['id'],
        fecha=entrenamiento_data['fecha'],
        distancia=entrenamiento_data['distancia'],
        tiempo=entrenamiento_data['tiempo'],
        calorias=entrenamiento_data['calorias'],
        usuario_id=entrenamiento_data['usuario_id'])
    print("Sincronizado " + entrenamiento)
    db.session.add(entrenamiento)
    db.session.commit()