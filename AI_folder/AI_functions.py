import sqlite3
from .SQL_comandos import *

def consulta(sql_: str='', pre_comando: str = '', dia_: str='', mes_: str='', ano_:str= '', outro_:str = '') -> list:
    try:
        # Log inicial dos parâmetros
        print("\n=== Iniciando Consulta ===")
        print(f"Parâmetros recebidos:")
        print(f"- SQL: {sql_}")
        print(f"- Pré-comando: {pre_comando}")
        print(f"- Dia: {dia_}")
        print(f"- Mês: {mes_}")
        print(f"- Ano: {ano_}")
        print(f"- Outro: {outro_}")
        
        # Construção da query
        if pre_comando != '':
            match pre_comando:
                case 'mes':
                    sql = mes
                    print("\nConstruindo query mensal...")
                    sql = sql.replace("WHERE strftime('%m', data_registro) = '09' ", f"WHERE strftime('%m', data_registro) = '{mes_}' ")
                    sql = sql.replace("AND strftime('%Y', data_registro) = '2024'", f"AND strftime('%Y', data_registro) = '{ano_}'")
                case 'ranking':
                    sql = ranking
                    print("\nConstruindo query de ranking...")
                    sql = sql.replace("AVG(temperatura) AS media ", f"AVG({outro_}) AS media ")
                    sql = sql.replace("strftime('%d', data_registro) = '10' ", f"strftime('%d', data_registro) = '{dia_}' ")
                    sql = sql.replace("AND strftime('%Y', data_registro) = '2024'", f"AND strftime('%Y', data_registro) = '{ano_}'")
                case 'dia':
                    sql = dia
                    print("\nConstruindo query diária...")
                    sql = sql.replace("WHERE DATE(d.data_registro) = '2024-05-21'", f"WHERE DATE(d.data_registro) = '{ano_}-{mes_}-{dia_}'")
        else:
            sql = rf'{sql_}'
            # Limpeza da string SQL
            replacements = {
                r'\"': '"',
                r"\'": "'",
                r"\\": "",
                r"\\'": "'",
                r'\n': ' '
            }
            for old, new in replacements.items():
                sql = sql.replace(old, new)

        print(f"\nSQL Final: {sql}")
        
        # Execução da query
        conexao = sqlite3.connect('instance/dados.db')
        c = conexao.cursor()
        c.execute(sql)
        resposta = c.fetchall()
        conexao.close()
        
        print(f"\nResultados obtidos: {len(resposta)} registros")
        print("Primeiros 3 registros (se houver):")
        for i, reg in enumerate(resposta[:3]):
            print(f"Registro {i+1}: {reg}")
            
        return resposta
        
    except Exception as e:
        print(f"\nERRO na consulta: {str(e)}")
        print("Stack trace:")
        import traceback
        traceback.print_exc()
        return []

class Motor:
    def __init__(self, nome, temperatura, corrente, vibracao):
        self.nome = nome
        self.temperatura = temperatura  # Temperatura média do braço (°C)
        self.corrente = corrente        # Corrente média do braço (A)
        self.vibracao = vibracao        # Vibração média do motor (mm/s²)
        self.vida_util_base_horas = 20000  # Vida útil base do motor (em horas)
        self.horas_fator = 0            # Horas previstas de operação até falha

    def calcular_vida_util(self):
        fator_temperatura = 1 + max(0, (self.temperatura - 80) / 10)  # Aumento a partir de 80°C
        fator_corrente = 1 + max(0, (self.corrente - 2) / 0.5)        # Aumento a partir de 2A
        fator_vibracao = 1 + max(0, (self.vibracao - 5) / 2)          # Aumento a partir de 5 mm/s²

        self.horas_fator = self.vida_util_base_horas / (fator_temperatura * fator_corrente * fator_vibracao)

    def calcular_chance_falha(self):
        self.calcular_vida_util()
        dias_ate_falha = self.horas_fator / 8  # Considerando 8 horas de operação por dia
        return dias_ate_falha

    def previsao_falha(self):
        dias_ate_falha = self.calcular_chance_falha()

        if dias_ate_falha < 0:
            return f"Possível falha do motor {self.nome} imediatamente."
        elif dias_ate_falha < 1:
            return f"Possível falha do motor {self.nome} em menos de 1 dia."
        elif dias_ate_falha < 250:
            return f"Possível falha do motor {self.nome} em {int(dias_ate_falha)} dias"
        else:
            return f"Não prevejo chance de falha para o motor {self.nome}"

class BracoRobotico:
    def __init__(self, temperatura_media, corrente_media, vibracoes):
        self.motores = [
            Motor("Base", temperatura_media, corrente_media, vibracoes[0]),
            Motor("Braço", temperatura_media, corrente_media, vibracoes[1]),
        ]

    def calcular_chance_total_falha(self):
        chances = [motor.calcular_chance_falha() for motor in self.motores]
        menor_tempo_falha = min(chances)
        if menor_tempo_falha < 0:
            return "Chance de falha do braço: 100.00%"
        elif menor_tempo_falha < 1:
            return "Chance de falha do braço: 100.00%"
        else:
            chance_falha_braco = max(0, (250 - menor_tempo_falha) / 250 * 100)
            return f"Chance de falha do braço: {chance_falha_braco:.2f}%"

    def prever_falhas(self):
        previsoes = [motor.previsao_falha() for motor in self.motores]
        return previsoes

def previsao(dia: str = '08', mes: str = '10', ano: str = '2024', msg_auto: bool = False):
    try:
        print("\n=== Iniciando Previsão ===")
        print(f"Parâmetros: dia={dia}, mes={mes}, ano={ano}, msg_auto={msg_auto}")
        
        # Validação básica dos parâmetros
        if not msg_auto:
            # Validar formato das datas
            if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
                raise ValueError("Dia, mês e ano devem ser números")
            if not (1 <= int(dia) <= 31 and 1 <= int(mes) <= 12):
                raise ValueError("Data inválida")
        
        # Construir a query apropriada
        if msg_auto:
            comando = """
            SELECT 
                temperatura,
                corrente,
                vibracao_base,
                vibracao_braco
            FROM 
                dados
            WHERE 
                data_registro IS NOT NULL
            ORDER BY 
                data_registro DESC
            LIMIT 1;
            """
        else:
            comando = f"""
            SELECT 
                AVG(temperatura) AS media_temperatura,
                AVG(corrente) AS media_corrente,
                AVG(vibracao_base) AS media_vibracao_base,
                AVG(vibracao_braco) AS media_vibracao_braco
            FROM 
                dados
            WHERE 
                DATE(data_registro) = '{ano}-{mes}-{dia}'
            AND
                data_registro IS NOT NULL;
            """
        
        print(f"\nExecutando consulta: {comando}")
        dados = consulta(comando)
        
        if not dados or not dados[0] or None in dados[0]:
            raise ValueError("Não foram encontrados dados válidos para o período especificado")
            
        print(f"\nDados obtidos: {dados}")
        temperatura, corrente, vibracao_base, vibracao_braco = dados[0]
        
        # Validação dos dados obtidos
        if any(not isinstance(x, (int, float)) for x in [temperatura, corrente, vibracao_base, vibracao_braco]):
            raise ValueError("Dados inválidos retornados da consulta")
            
        braco = BracoRobotico(temperatura, corrente, [vibracao_base, vibracao_braco])
        previsoes = braco.prever_falhas()
        chance_total = braco.calcular_chance_total_falha()
        
        print("\nResultados da previsão:")
        print(f"Chance total: {chance_total}")
        print(f"Previsões: {previsoes}")
        
        return chance_total, previsoes
        
    except Exception as e:
        print(f"\nERRO na previsão: {str(e)}")
        print("Stack trace:")
        import traceback
        traceback.print_exc()
        return "Erro ao calcular previsão", []

def meses():
    return consulta("SELECT DISTINCT strftime('%m', data_registro) AS mes FROM dados WHERE data_registro IS NOT NULL ORDER BY mes;")

def fetch_data(filters):
    query = "SELECT"
    if filters['timeRange'] == 'day':
        query += " strftime('%H', data_registro) AS time,"
    elif filters['timeRange'] == 'week':
        query += " strftime('%d', data_registro) AS time,"
    elif filters['timeRange'] == 'month':
        query += " strftime('%W', data_registro) AS time,"
    elif filters['timeRange'] == 'year':
        query += " strftime('%m', data_registro) AS time,"
    
    query += """
        AVG(vibracao_braco) AS vibracao_braco,
        AVG(vibracao_base) AS vibracao_base,
        AVG(corrente) AS corrente,
        AVG(temperatura) AS temperatura
        FROM dados
    """
    
    if filters['timeRange'] == 'day':
        query += " WHERE strftime('%Y-%m-%d', data_registro) = '{}'".format(filters['day'])
    elif filters['timeRange'] == 'week':
        query += " WHERE strftime('%Y-%W', data_registro) = '{}'".format(filters['week'])
    elif filters['timeRange'] == 'month':
        query += " WHERE strftime('%Y-%m', data_registro) = '{}'".format(filters['month'])
    elif filters['timeRange'] == 'year':
        query += " WHERE strftime('%Y', data_registro) = '{}'".format(filters['year'])

    query += " GROUP BY time ORDER BY time ASC"
    
    data = consulta(query)
    print("Dados retornados pela consulta:", data)
    return data
