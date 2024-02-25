import redis
from flask import Flask
import datetime
import json

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
    return 'Hola, soy el monitor'

servicioMonitor = r.pubsub()
servicioMonitor.subscribe('EstadoSalud')

for message in servicioMonitor.listen():
    print(message) 
    # msg_json = json.loads(str(message['data']))
    msg_json = str(message['data'])
    message_rta = {'Ping_recibido' : msg_json, 'Fecha' : str(datetime.datetime.now())}
    r.publish("RespuestadeEstadoSalud", str(message_rta))