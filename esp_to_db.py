import sqlite3
import os

# Replace or add this configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
if app.config['SQLALCHEMY_DATABASE_URI'] and app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
