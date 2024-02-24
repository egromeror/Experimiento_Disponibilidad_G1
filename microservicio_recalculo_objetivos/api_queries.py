from .app import Entrenamiento, EntrenamientoSchema, Resource

entrenamiento_schema = EntrenamientoSchema()

class EntrenamientoResourceQ(Resource):
    def get(self):
        entrenamientos = Entrenamiento.query.all()
        return entrenamiento_schema.dump(entrenamientos, many=True)