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
    s: int = 1
    e: int = 101
    for i in range(s, e, 1):
        message = "Ping: " + str(i) + " de "+ str(e-1)
        print(message)
        i=i+1
        r.publish("EstadoSalud", message)
        if i==e:
            exit()