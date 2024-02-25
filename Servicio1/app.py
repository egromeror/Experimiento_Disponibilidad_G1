import redis
from flask import Flask


app = Flask(__name__)

app_context = app.app_context()
app_context.push()

r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=True
)


@app.route('/')
def hello():
    return 'Hola, soy el microservicio 1'

while True:
    message = input("Ingrese el mensaje: ")

    r.publish("EstadoSalud", message)