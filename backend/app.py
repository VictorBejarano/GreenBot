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

# Archivo para guardar los datos
DATA_FILE = "bluetooth_data.json"

# Dirección MAC y puerto del dispositivo Bluetooth
HC05_MAC = "00:22:11:30:CF:07"  # Cambia a la dirección MAC de tu HC-05
PORT = 1

# Variable global para el socket Bluetooth
bluetooth_socket = None

# Función para leer JSON completo usando delimitadores
def read_valid_json(sock):
    buffer = ""
    while True:
        try:
            data = sock.recv(1024).decode("utf-8")
            buffer += data.strip()
            start_idx = buffer.find("<<")
            end_idx = buffer.find(">>")
            if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                json_string = buffer[start_idx + 2:end_idx].strip()
                try:
                    json_data = json.loads(json_string)
                    buffer = buffer[end_idx + 2:]
                    return json_data
                except json.JSONDecodeError as e:
                    logger.error(f"Error al decodificar JSON: {e}")
                    buffer = buffer[end_idx + 2:]
            else:
                logger.warning("Esperando mensaje completo...")
        except Exception as e:
            logger.error(f"Error al leer del socket: {e}")
            break

# Función para agregar la fecha y hora al JSON
def add_timestamp_to_json(json_data):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    json_data['timestamp'] = timestamp
    return json_data

# Guardar datos en un archivo
def save_data_to_file(data):
    try:
        with open(DATA_FILE, "a") as file:
            file.write(json.dumps(data) + "\n")
        logger.info(f"Dato guardado en el archivo: {data}")
    except Exception as e:
        logger.error(f"Error al guardar datos en el archivo: {e}")

# Leer los últimos 150 datos del archivo
def get_last_150_data():
    try:
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
            last_150 = lines[-150:] if len(lines) >= 150 else lines
            return [json.loads(line.strip()) for line in last_150]
    except FileNotFoundError:
        logger.warning("El archivo de datos no existe aún.")
        return []
    except Exception as e:
        logger.error(f"Error al leer los datos del archivo: {e}")
        return []

# Conectar al dispositivo Bluetooth
def connect_to_bluetooth():
    global bluetooth_socket
    try:
        bluetooth_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        bluetooth_socket.connect((HC05_MAC, PORT))
        logger.info(f"Conectado a {HC05_MAC}")
        return bluetooth_socket
    except bluetooth.BluetoothError as e:
        logger.error(f"No se pudo conectar al dispositivo Bluetooth: {e}")
        return None

# Transmitir datos Bluetooth
def bluetooth_data_stream(sock):
    try:
        while True:
            comando = "LEER"
            sock.send(comando)
            logger.info(f"Comando enviado: {comando}")
            json_data = read_valid_json(sock)
            if json_data:
                json_data_with_timestamp = add_timestamp_to_json(json_data)
                save_data_to_file(json_data_with_timestamp)
                socketio.emit('data_update', {'data': json_data_with_timestamp})
                logger.info(f"Dato transmitido: {json_data_with_timestamp}")
            eventlet.sleep(5)
    except bluetooth.btcommon.BluetoothError as e:
        logger.error(f"Error en la transmisión de Bluetooth: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    logger.info('Cliente conectado')
    emit('message', {'data': 'Conexión establecida con el servidor'})

@socketio.on('get_last_150_data')
def handle_get_last_150_data(data):
    last_150_data = get_last_150_data()
    emit('last_150_data', {'data': last_150_data})
    logger.info(f"Últimos 150 datos enviados al cliente.")

@socketio.on('start_bluetooth_stream')
def handle_bluetooth_stream(data):
    global bluetooth_socket
    if not bluetooth_socket:
        bluetooth_socket = connect_to_bluetooth()
    if bluetooth_socket:
        socketio.start_background_task(bluetooth_data_stream, bluetooth_socket)
        emit('message', {'data': 'Iniciando transmisión de datos Bluetooth'})
    else:
        emit('message', {'data': 'No se pudo conectar al dispositivo Bluetooth'})

# Función para manejar el envío de comandos en segundo plano
def send_bluetooth_command(command):
    global bluetooth_socket
    if bluetooth_socket:
        try:
            bluetooth_socket.send(command)
            logger.info(f"Comando enviado al Arduino: {command}")
            return True
        except bluetooth.BluetoothError as e:
            logger.error(f"Error al enviar comando: {e}")
            return False
    else:
        logger.warning("No hay conexión Bluetooth activa")
        return False

@socketio.on('activate_fan')
def handle_activate_fan(data):
    logger.info("Recibido evento: activate_fan")
    socketio.start_background_task(send_bluetooth_command, "ACTIVAR_VENTILADOR")
    emit('message', {'data': 'Intentando activar el ventilador...'})

@socketio.on('desactivate_fan')
def handle_desactivate_fan(data):
    logger.info("Recibido evento: desactivate_fan")
    socketio.start_background_task(send_bluetooth_command, "DESACTIVAR_VENTILADOR")
    emit('message', {'data': 'Intentando desactivar el ventilador...'})

@socketio.on('activate_luz')
def handle_activate_luz(data):
    logger.info("Recibido evento: activate_luz")
    socketio.start_background_task(send_bluetooth_command, "ACTIVAR_LUZ")
    emit('message', {'data': 'Intentando activar la luz...'})

@socketio.on('desactivate_luz')
def handle_desactivate_luz(data):
    logger.info("Recibido evento: desactivate_luz")
    socketio.start_background_task(send_bluetooth_command, "DESACTIVAR_LUZ")
    emit('message', {'data': 'Intentando desactivar la luz...'})


# Iniciar servidor
if __name__ == '__main__':
    bluetooth_socket = connect_to_bluetooth()
    if bluetooth_socket:
        socketio.start_background_task(bluetooth_data_stream, bluetooth_socket)
        logger.info("Transmisión de datos Bluetooth iniciada automáticamente.")
    else:
        logger.error("No se pudo iniciar la transmisión de datos Bluetooth automáticamente.")

    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
