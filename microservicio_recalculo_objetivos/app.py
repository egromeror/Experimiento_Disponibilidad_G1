from microservicio_recalculo_objetivos import create_app
from flask_restful import Api, Resource
from redis import Redis
from rq import Queue
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .modelos import Entrenamiento, EntrenamientoSchema,db
from datetime import datetime
# from microservicio_recalculo_objetivos.api_commands import EntrenamientoResourceC
from microservicio_recalculo_objetivos.api_queries import EntrenamientoResourceQ
# from microservicio_recalculo_objetivos import sender

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
entrenamiento_schema = EntrenamientoSchema()

q = Queue(connection=Redis(host='localhost', port=6379, db=0))

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

def send_entrenamiento(entrenamiento_data):
    pass

api.add_resource(EntrenamientoResourceC, '/api-commands/entrenamientos')
api.add_resource(EntrenamientoResourceQ, '/api-queries/entrenamientos')

# with app.app_context():
#     entrenamiento = Entrenamiento(fecha=datetime.now(), distancia=10, tiempo=60, calorias=500, usuario_id=1)
#     db.session.add(entrenamiento)
#     db.session.commit()
