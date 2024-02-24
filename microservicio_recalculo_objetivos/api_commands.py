from microservicio_recalculo_objetivos.app import db, Entrenamiento, EntrenamientoSchema, Resource, request, Redis, Queue, datetime
from microservicio_recalculo_objetivos.sender import send_entrenamiento

q = Queue(connection=Redis(host='localhost', port=6379, db=0))
entrenamiento_schema = EntrenamientoSchema()

class EntrenamientoResourceC(Resource):
    def post(self):
        new_entrenamiento = Entrenamiento(
            fecha=datetime.strptime(request.json['fecha'], '%y-%m-%d %H:%M:%S'),
            distancia=request.json['distancia'],
            tiempo=request.json['tiempo'],
            calorias=request.json['calorias'],
            usuario_id=request.json['usuario_id']
        )
        db.session.add(new_entrenamiento)
        db.session.commit()
        q.enqueue(send_entrenamiento, entrenamiento_schema.dump(new_entrenamiento))
        return entrenamiento_schema.dump(new_entrenamiento)