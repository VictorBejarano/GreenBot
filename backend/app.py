import logging
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import bluetooth  # Importa pybluez para manejar conexiones Bluetooth
import eventlet
import time

# Configuración del logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", ping_interval=10, ping_timeout=20)  # Permitir todos los orígenes

# Función para agregar encabezados CORS
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

# Dirección MAC y puerto del dispositivo Bluetooth
HC05_MAC = "20:16:04:19:08:81"  # Cambia a la dirección MAC de tu HC-05
PORT = 1

# Conectar al dispositivo Bluetooth
def connect_to_bluetooth():
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((HC05_MAC, PORT))
        logger.info(f"Conectado a {HC05_MAC}")
        return sock
    except bluetooth.BluetoothError as e:
        logger.error(f"No se pudo conectar al dispositivo Bluetooth: {e}")
        return None

# Envía comandos periódicos al Arduino y lee la respuesta
def bluetooth_data_stream(sock):
    try:
        while True:
            comando = "LEER"  # Comando que se envía al Arduino
            sock.send(comando)
            logger.info(f"Comando enviado: {comando}")
            data = sock.recv(1024).decode("utf-8").strip()  # Decodifica la respuesta del Arduino
            logger.info(f"Dato recibido: {data}")
            socketio.emit('data_update', {'data': data})
            logger.info(f"Evento 'data_update' emitido con los datos: {data}")
            eventlet.sleep(5)  # Espera 5 segundos antes de enviar otro comando, usando eventlet.sleep
    except bluetooth.btcommon.BluetoothError as e:
        logger.error(f"Error en la transmisión de Bluetooth: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    logger.info('Cliente conectado')
    emit('message', {'data': 'Conexión establecida con el servidor'})

@socketio.on('start_bluetooth_stream')
def handle_bluetooth_stream(data):
    sock = connect_to_bluetooth()
    if sock:
        # En lugar de usar threading, usamos eventlet para ejecutar la función en segundo plano
        socketio.start_background_task(bluetooth_data_stream, sock)
        emit('message', {'data': 'Iniciando transmisión de datos Bluetooth'})
    else:
        emit('message', {'data': 'No se pudo conectar al dispositivo Bluetooth'})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)