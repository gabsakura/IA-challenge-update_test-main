import sqlite3

def verificar_tabela():
    conn = sqlite3.connect('instance/dados.db')  # Ajuste o caminho se necessário
    cursor = conn.cursor()

    # Listando todas as tabelas no banco de dados
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()

    print("Tabelas existentes no banco de dados:")
    for tabela in tabelas:
        print(tabela[0])

    conn.close()

verificar_tabela()
