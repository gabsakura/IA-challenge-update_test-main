import sqlite3

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
