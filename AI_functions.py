import ast
import pickle
import sqlite3
import numpy as np
from sklearn.preprocessing import StandardScaler

def consulta(sql: str) -> list:
    sql = rf'{sql}'
    raw = r'\"'
    raw2 = r"\'"
    raw3 = r"\\"
    raw4 = r"\\'"

    if r'\"' in sql:
        sql = sql.replace(raw, '"')
    if r"\'" in sql:
        sql = sql.replace(raw2, "'")
    if r"\\" in sql:
        sql = sql.replace(raw3, "")
    if r"\\'" in sql:
        sql = sql.replace(raw4, "'")

    if r'\n' in sql:
        sql = sql.replace(r'\n', '')

    #print(sql)
    #print("----------------------")

    try:
        conexao = sqlite3.connect('dados.db', check_same_thread=False)
        c = conexao.cursor()
        c.execute(sql)
        resposta = c.fetchall()
        conexao.close()
        #print("Requisição feita \n----------------------")
        return resposta
    except:
        return []
    
def previsao(dia: str = '09', mes: str = '08', ano: str = '2024', msg_auto: bool = False) -> list:
    def prever_falha(modelo, dados):
        scaler = StandardScaler()
        dados_scaled = scaler.fit_transform(dados)
        probabilidades = modelo.predict_proba(dados_scaled)[:, 1]  # Probabilidade da classe 1
        return probabilidades

    with open("modelo_previsao.pkl", "rb") as arquivo:
        modelo = pickle.load(arquivo)

    lista_previsoes = list()

    if not msg_auto:
        comando_sql = f"""
        SELECT 
            sensor_id, 
            '[' || GROUP_CONCAT('[' || temperatura || ',' || corrente || ',' || vibracao || ',' || umidade || ']', ',') || ']' AS sensor_data
        FROM 
            dados 
        WHERE 
            DATE(timestamp) = '{ano}-{mes}-{dia}'
        GROUP BY 
            sensor_id
        ORDER BY 
            sensor_id;
        """
    else:
        comando_sql = """
        WITH UltimaLeituraGlobal AS (
            SELECT 
                MAX(timestamp) AS ultima_leitura
            FROM 
                dados 
            WHERE 
                DATE(timestamp) = DATE('now')  -- Considera a data atual
        )

        SELECT 
            sensor_id, 
            GROUP_CONCAT(
            '[' || temperatura || ',' || corrente || ',' || vibracao || ',' || umidade || ']', 
            ',' 
            ) AS sensor_data
        FROM 
            dados d
        JOIN 
            UltimaLeituraGlobal ul
        ON 
            d.timestamp BETWEEN datetime(ul.ultima_leitura, '-1 hour') AND ul.ultima_leitura  -- Intervalo de 1 hora antes da última leitura global
        WHERE 
            DATE(d.timestamp) = DATE('now')  -- Considera a data atual
        GROUP BY 
            sensor_id
        ORDER BY 
            sensor_id;
        """

    r_dados = consulta(comando_sql)

    try:
        lista = ast.literal_eval(r_dados)
    except:
        return '[]'

    dados = [(sensor_id, ast.literal_eval(sensor_data)) for sensor_id, sensor_data in lista]

    if not dados:
        return '[]'
    else:
        for i in range(len(dados)):
            dados_transformados = np.array(dados[i][1])

            probabilidades = prever_falha(modelo, dados_transformados)

            lista_previsoes.append(round(sum(probabilidades) / len(probabilidades) * 100, 2))

        return str(lista_previsoes)
