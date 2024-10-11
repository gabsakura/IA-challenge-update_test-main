import sqlite3

def criar_tabela():
    conn = sqlite3.connect('instance/dados.db')
    cursor = conn.cursor()
    
    # Criando a tabela "dados" se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            corrente REAL,
            vibracao REAL,
            temperatura REAL
        )
    ''')
    
    conn.commit()
    conn.close()

# Chamar a função para criar a tabela
criar_tabela()
