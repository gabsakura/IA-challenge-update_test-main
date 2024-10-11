from flask import Flask, request
import mysql.connector
from datetime import datetime  # Importa a biblioteca para lidar com datas e horas

app = Flask(__name__)

# Conexão ao banco de dados MySQL
conn = mysql.connector.connect(
    host="20.50.193.74",
    user="root",
    password="Batatinha123",
    database="sensores_db"
)

@app.route('/sensores', methods=['POST'])
def receive_data():
    data = request.json
    cursor = conn.cursor()

    # Gera o timestamp atual no momento da inserção
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # SQL para inserir dados, sem precisar passar o timestamp na requisição
    sql = "INSERT INTO dados (sensor_id, temperatura, corrente, vibracao, umidade, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (data['sensor_id'], data['temperatura'], data['corrente'], data['vibracao'], data['umidade'], timestamp)
    
    cursor.execute(sql, values)
    conn.commit()
    return "Dados inseridos com sucesso!", 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
