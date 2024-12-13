import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure database
database_url = os.getenv('DATABASE_URL')

# If using Render's PostgreSQL, fix the URL if needed
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///instance/dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Conectar ao banco de dados
conn = sqlite3.connect('instance/dados.db')
cursor = conn.cursor()

# Nome do usuário que você deseja promover a admin
username = '123'

# Atualizar o status de admin
cursor.execute('UPDATE user SET is_admin = 1 WHERE username = ?;', (username,))

# Commit e fechar a conexão
conn.commit()
conn.close()
