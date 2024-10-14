# from flask import Flask, jsonify, request
# from influxdb_client import InfluxDBClient

# app = Flask(__name__)

# # Configuración de InfluxDB
# token = "your-influxdb-token"
# org = "your-org"
# bucket = "your-bucket"
# url = "http://influxdb:8086"

# client = InfluxDBClient(url=url, token=token, org=org)
# query_api = client.query_api()

# @app.route('/data', methods=['GET'])
# def get_data():
#     query = '{"response": "Hi"}'
    
#     return jsonify(query), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

from flask import Flask, jsonify, request
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configuración del pin
LED_PIN = 18  # Cambia esto al número de pin GPIO que estés utilizando
GPIO.setmode(GPIO.BCM)  # Usa la numeración BCM
GPIO.setup(LED_PIN, GPIO.OUT)  # Configura el pin como salida

@app.route('/led', methods=['POST'])
def control_led():
    data = request.get_json()
    action = data.get('action')

    if action == 'on':
        GPIO.output(LED_PIN, GPIO.HIGH)  # Enciende el LED
        return jsonify({'status': 'LED encendido'}), 200
    elif action == 'off':
        GPIO.output(LED_PIN, GPIO.LOW)  # Apaga el LED
        return jsonify({'status': 'LED apagado'}), 200
    else:
        return jsonify({'error': 'Acción no válida'}), 400

@app.route('/shutdown', methods=['GET'])
def shutdown():
    GPIO.cleanup()  # Limpia la configuración de GPIO
    return jsonify({'status': 'Apagando la Raspberry Pi'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)