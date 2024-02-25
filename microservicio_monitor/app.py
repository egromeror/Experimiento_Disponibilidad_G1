import redis
from flask import Flask
import datetime 
import time
import threading
import random
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
    return 'Hola, soy el microservicio 1'

class RespuestaEstadoSalud:
   def __init__(self, nombre, tiempo, respuesta):
    self.nombre = nombre
    self.tiempo = tiempo
    self.respuesta = respuesta

def generar_respuesta_error():
    numeros = [1, 2]
    numero_aleatorio = random.choice(numeros)
    return numero_aleatorio

cantidadTotal = 5
numFallos = 2
i = 1
def send_ping_estadosalud():
    for i in range(cantidadTotal):
        numero = 3
        if i >= (cantidadTotal - numFallos):
            numero = generar_respuesta_error()
        
        estado_salud = RespuestaEstadoSalud('MicroservicioDiagnostico', 0, numero)       
        print(json.dumps(estado_salud.__dict__))
        r.publish("EstadoMicroservicioDiagnostico", json.dumps(estado_salud.__dict__))


i = 1
def send_ping_estadorecalculo():
    for i in range(cantidadTotal):
        numero = 3
        if i >= (cantidadTotal - numFallos):
            numero = generar_respuesta_error()
        
        estado_salud = RespuestaEstadoSalud('MicroservicioRecalculo', 0, numero)       
        print(json.dumps(estado_salud.__dict__))
        r.publish("EstadoMicroservicioRecalculo", json.dumps(estado_salud.__dict__))

def get_response_diagnostico():
    servicioMonitor = r.pubsub()
    servicioMonitor.subscribe('RTA_EstadoMicroservicioDiagnostico')
    for message in servicioMonitor.listen():
        msg_json = str(message['data'])
        message_rta = {'Ping_recibido' : msg_json, 'Fecha' : str(datetime.datetime.now())}
        print(message_rta)

def get_response_recalculo():
    servicioMonitor = r.pubsub()
    servicioMonitor.subscribe('RTA_EstadoMicroservicioRecalculo')
    for message in servicioMonitor.listen():
        msg_json = str(message['data'])
        message_rta = {'Ping_recibido' : msg_json, 'Fecha' : str(datetime.datetime.now())}
        print(message_rta)

t1 = threading.Thread(target=send_ping_estadosalud)
t1.start()
t2 = threading.Thread(target=send_ping_estadorecalculo)
t2.start()
t3 = threading.Thread(target=get_response_diagnostico)
t3.start()
t4 = threading.Thread(target=get_response_recalculo)
t4.start()
#while True:
    