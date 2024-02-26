import redis
from flask import Flask
import datetime
import json
import time

app = Flask(__name__)

app_context = app.app_context()
app_context.push()

r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=True
)

class RespuestaEstadoSalud:
   def __init__(self, nombre, tiempo, respuesta):
    self.nombre = nombre
    self.tiempo = tiempo
    self.respuesta = respuesta

@app.route('/')
def hello():
    return 'Hola, soy el microservicio de diagnostico de estado medico de salud'

servicioMonitor = r.pubsub()
servicioMonitor.subscribe('EstadoMicroservicioDiagnostico')

for message in servicioMonitor.listen():
    print(message) 
    tiempo_inicial = time.time()

    try: 
         numero = json.loads(message['data']).get('respuesta')
    except:
         numero = 1

    if numero == 1:
        time.sleep(2)   
    
    if numero == 2:
        time.sleep(5)
    
    if numero == 3:
        time.sleep(1)
    
    tiempo_final = time.time()   
    
    estado_salud = RespuestaEstadoSalud('RTA_MicroservicioDiagnostico', (tiempo_final-tiempo_inicial), numero)       
    if(numero == 3 or numero == 2):
        r.publish("RTA_EstadoMicroservicioDiagnostico", json.dumps(estado_salud.__dict__))