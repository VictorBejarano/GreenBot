from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient

app = Flask(__name__)

# Configuración de InfluxDB
token = "your-influxdb-token"
org = "your-org"
bucket = "your-bucket"
url = "http://influxdb:8086"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

@app.route('/data', methods=['GET'])
def get_data():
    query = f'from(bucket: "{bucket}") |> range(start: -1h)'
    result = query_api.query(org=org, query=query)
    
    data = [{"time": record.get_time(), "value": record.get_value()} for record in result]
    
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)