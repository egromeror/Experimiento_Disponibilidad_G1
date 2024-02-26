import redis
from flask import Flask
from datetime import datetime, timedelta 
import time
import threading
import random
import json
import logging

app = Flask(__name__)

app_context = app.app_context()
app_context.push()

logmonitor= logging
logmonitor.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

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
        
        logmonitor.info(f"Mensaje enviado a microservicio diagnostico correctamente: {json.dumps(estado_salud.__dict__)}")
        print(json.dumps(estado_salud.__dict__))
        r.publish("EstadoMicroservicioDiagnostico", json.dumps(estado_salud.__dict__))


i = 1
def send_ping_estadorecalculo():
    for i in range(cantidadTotal):
        numero = 3
        if i >= (cantidadTotal - numFallos):
            numero = generar_respuesta_error()
        
        estado_salud = RespuestaEstadoSalud('MicroservicioRecalculo', 0, numero)       

        logmonitor.info(f"Mensaje enviado a microservicio recalculo correctamente: {json.dumps(estado_salud.__dict__)}")
        print(json.dumps(estado_salud.__dict__))
        r.publish("EstadoMicroservicioRecalculo", json.dumps(estado_salud.__dict__))

i = 1
def send_ping_estadodetener():
    for i in range(cantidadTotal):
        numero = 3
        if i >= (cantidadTotal - numFallos):
            numero = generar_respuesta_error()
        
        estado_salud = RespuestaEstadoSalud('MicroservicioDetener', 0, numero)       

        logmonitor.info(f"Mensaje enviado a microservicio detener correctamente: {json.dumps(estado_salud.__dict__)}")
        print(json.dumps(estado_salud.__dict__))
        r.publish("EstadoMicroservicioDetener", json.dumps(estado_salud.__dict__))

def get_response_diagnostico():
    servicioMonitor = r.pubsub()
    servicioMonitor.subscribe('RTA_EstadoMicroservicioDiagnostico')
    try:
        for message in servicioMonitor.listen():
            try:
                try:
                    message_data = json.loads(message['data'])
                except:
                    continue

                print(message_data)
                time_received = message_data['tiempo']
                                
                if time_received > 3:
                    logmonitor.error(f"Error: el tiempo es mayor a 2 segundos. Mensaje: {message['data']}")
                else:
                    logmonitor.info(f"Mensaje de microservicio diagnostico recibido correctamente: {message['data']}")
                
            except json.JSONDecodeError:
                logmonitor.error(f"Error al decodificar JSON: {message['data']}")
            except KeyError:
                logmonitor.error(f"Atributo 'time' no encontrado en el mensaje: {message['data']}")
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
        logmonitor.error(f"Error de conexión con Redis: {e}")

def get_response_recalculo():
    servicioMonitor = r.pubsub()
    servicioMonitor.subscribe('RTA_EstadoMicroservicioRecalculo')
    try:
        for message in servicioMonitor.listen():
            try:
                try:
                    message_data = json.loads(message['data'])
                except:
                    continue

                print(message_data)
                time_received = message_data['tiempo']
                                
                if time_received > 3:
                    logmonitor.error(f"Error: el tiempo es mayor a 2 segundos. Mensaje: {message['data']}")
                else:
                    logmonitor.info(f"Mensaje de microservicio recalculo recibido correctamente: {message['data']}")
                
            except json.JSONDecodeError:
                logmonitor.error(f"Error al decodificar JSON: {message['data']}")
            except KeyError:
                logmonitor.error(f"Atributo 'time' no encontrado en el mensaje: {message['data']}")
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
        logmonitor.error(f"Error de conexión con Redis: {e}")

def get_response_detener():
    servicioMonitor = r.pubsub()
    servicioMonitor.subscribe('RTA_EstadoMicroservicioDetener')
    try:
        for message in servicioMonitor.listen():
            try:
                try:
                    message_data = json.loads(message['data'])
                except:
                    continue

                print(message_data)
                time_received = message_data['tiempo']
                                
                if time_received > 3:
                    logmonitor.error(f"Error: el tiempo es mayor a 2 segundos. Mensaje: {message['data']}")
                else:
                    logmonitor.info(f"Mensaje de microservicio detener recibido correctamente: {message['data']}")
                
            except json.JSONDecodeError:
                logmonitor.error(f"Error al decodificar JSON: {message['data']}")
            except KeyError:
                logmonitor.error(f"Atributo 'time' no encontrado en el mensaje: {message['data']}")
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
        logmonitor.error(f"Error de conexión con Redis: {e}")

t1 = threading.Thread(target=send_ping_estadosalud)
t2 = threading.Thread(target=send_ping_estadorecalculo)
t3 = threading.Thread(target=get_response_diagnostico)
t4 = threading.Thread(target=get_response_recalculo)
t5 = threading.Thread(target=send_ping_estadodetener)
t6 = threading.Thread(target=get_response_detener)
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()

#while True:
    