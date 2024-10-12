import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('instance/dados.db')
cursor = conn.cursor()

# Deletar a tabela inteira (por exemplo, 'tabela3')
cursor.execute('ALTER TABLE dados RENAME COLUMN vibração_base TO vibracao_base')

# Confirmar a operação
conn.commit()

# Fechar a conexão
conn.close()
