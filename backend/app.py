import logging
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import bluetooth  # Importa pybluez para manejar conexiones Bluetooth
import eventlet
import time
import json
from datetime import datetime

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

# Función para leer JSON completo usando delimitadores
def read_valid_json(sock):
    buffer = ""  # Búfer para acumular los datos recibidos
    while True:
        try:
            # Lee los datos y acumúlalos en el búfer
            data = sock.recv(1024).decode("utf-8")
            buffer += data.strip()
            
            # Busca el mensaje completo delimitado por `<<` y `>>`
            start_idx = buffer.find("<<")
            end_idx = buffer.find(">>")
            
            # Verifica que el mensaje esté completo (tiene delimitadores de inicio y fin)
            if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                json_string = buffer[start_idx + 2:end_idx].strip()  # Extrae el JSON entre los delimitadores
                
                # Intenta convertir el string JSON a un diccionario
                try:
                    json_data = json.loads(json_string)
                    buffer = buffer[end_idx + 2:]  # Elimina el mensaje procesado del búfer
                    return json_data
                except json.JSONDecodeError as e:
                    logger.error(f"Error al decodificar JSON: {e}")
                    buffer = buffer[end_idx + 2:]  # Descarta el mensaje inválido y sigue leyendo
            else:
                logger.warning("Esperando mensaje completo...")
        except Exception as e:
            logger.error(f"Error al leer del socket: {e}")
            break

# Función para agregar la fecha y hora al JSON
def add_timestamp_to_json(json_data):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Formato de fecha y hora
    json_data['timestamp'] = timestamp
    return json_data

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
            json_data = read_valid_json(sock) 
            json_data_with_timestamp = add_timestamp_to_json(json_data)
            logger.info(f"Dato recibido: {json_data_with_timestamp}")
            socketio.emit('data_update', {'data': json_data_with_timestamp})
            logger.info(f"Evento 'data_update' emitido con los datos: {json_data_with_timestamp}")
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

# Conexión y transmisión automática al inicio del programa
if __name__ == '__main__':
    sock = connect_to_bluetooth()
    if sock:
        # Inicia el hilo de transmisión de datos Bluetooth automáticamente
        socketio.start_background_task(bluetooth_data_stream, sock)
        logger.info("Transmisión de datos Bluetooth iniciada automáticamente.")
    else:
        logger.error("No se pudo iniciar la transmisión de datos Bluetooth automáticamente.")

    # Inicia el servidor SocketIO
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
