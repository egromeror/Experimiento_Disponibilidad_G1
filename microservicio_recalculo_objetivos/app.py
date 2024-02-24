from flask import Flask
from flask_restful import Api, Resource
from redis import Redis
from rq import Queue
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .modelos import Entrenamiento, EntrenamientoSchema,db
from datetime import datetime
from .api_commands import EntrenamientoResourceC
from .api_queries import EntrenamientoResourceQ

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entrenamientos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

api.add_resource(EntrenamientoResourceC, '/api-commands/entrenamientos')
api.add_resource(EntrenamientoResourceQ, '/api-queries/entrenamientos')

# with app.app_context():
#     entrenamiento = Entrenamiento(fecha=datetime.now(), distancia=10, tiempo=60, calorias=500, usuario_id=1)
#     db.session.add(entrenamiento)
#     db.session.commit()
