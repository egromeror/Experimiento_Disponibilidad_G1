import redis
from flask import Flask
import datetime 
import time
import threading

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

def send_ping():
    for i in range(s, e):
        message = {'Ping_Estado' : i, 'Fecha' : str(datetime.datetime.now())}
        print(message)
        i=i+1
        r.publish("EstadoSalud", str(message))
        time.sleep(3)
        if i == e:
            exit()



s: int = 1
e: int = 101
t1 = threading.Thread(target=send_ping)
t1.start()
while True:
    servicioMonitor = r.pubsub()
    servicioMonitor.subscribe('RespuestadeEstadoSalud')
    for message in servicioMonitor.listen():
        msg_json = str(message['data'])
        message_rta = {'Ping_recibido' : msg_json, 'Fecha' : str(datetime.datetime.now())}
        print(message_rta) 
    