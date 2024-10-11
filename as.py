import sqlite3

def get_dados():
    try:
        conn = sqlite3.connect('instance/dados.db')
        cursor = conn.cursor()
        cursor.execute("SELECT corrente, vibracao, temperatura FROM dados")
        rows = cursor.fetchall()
        conn.close()

        corrente = [row[0] for row in rows]
        vibracao = [row[1] for row in rows]
        temperatura = [row[2] for row in rows]
        labels = [f'Item {i+1}' for i in range(len(rows))]

        # Mostrar um dos dados obtidos
        print(f"Primeiro dado de corrente: {corrente[0]}")
        
        return {
            'corrente': corrente,
            'vibracao': vibracao,
            'temperatura': temperatura,
            'labels': labels
        }
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Verificar a conexão
dados = get_dados()
if dados is not None:
    print("Conexão bem-sucedida e dados obtidos!")
else:
    print("Falha na conexão com o banco de dados.")
