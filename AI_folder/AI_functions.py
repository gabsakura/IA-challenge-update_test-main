import sqlite3
from .SQL_comandos import *

def consulta(sql_: str='', pre_comando: str = '', dia_: str='', mes_: str='', ano_:str= '', outro_:str = '') -> list:
    print(f"sql_: {sql_}")
    print(f"pre_comando: {pre_comando}")
    print(f"dia_: {dia_}")
    print(f"mes_: {mes_}")
    print(f"ano_: {ano_}")
    print(f"outro_: {outro_}")
    
    if pre_comando != '':
        match pre_comando:
            case 'mes':
                sql = mes
                sql = sql.replace("WHERE strftime('%m', data_registro) = '09' ", f"WHERE strftime('%m', data_registro) = '{mes_}' ")
                sql = sql.replace("AND strftime('%Y', data_registro) = '2024'", f"AND strftime('%Y', data_registro) = '{ano_}'")
            case 'ranking':
                sql = ranking
                sql = sql.replace("AVG(temperatura) AS media ", f"AVG({outro_}) AS media ")
                sql = sql.replace("strftime('%d', data_registro) = '10' ", f"strftime('%d', data_registro) = '{dia_}' ")
                sql = sql.replace("AND strftime('%Y', data_registro) = '2024'", f"AND strftime('%Y', data_registro) = '{ano_}'")
            case 'dia':
                sql = dia
                sql = sql.replace("WHERE DATE(d.data_registro) = '2024-05-21'", f"WHERE DATE(d.data_registro) = '{ano_}-{mes_}-{dia_}'")
    else:
        sql = rf'{sql_}'
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

    print(sql)
    print("----------------------")
    # Mude o nome do banco de dados aqui
    conexao = sqlite3.connect('instance/dados.db')
    c = conexao.cursor()
    c.execute(sql)
    resposta = c.fetchall()
    conexao.close()
    print("Requisição feita \n----------------------")
    
    print(resposta)  # Adicione esta linha para ver o que a função está retornando
    return resposta

class Motor:
    def __init__(self, nome, temperatura, corrente, vibracao):
        self.nome = nome
        self.temperatura = temperatura  # Temperatura média do braço (°C)
        self.corrente = corrente        # Corrente média do braço (A)
        self.vibracao = vibracao        # Vibração média do motor (mm/s²)
        self.vida_util_base_horas = 20000  # Vida útil base do motor (em horas)
        self.horas_fator = 0            # Horas previstas de operação até falha

    def calcular_vida_util(self):
        # Cálculo dos fatores de impacto
        fator_temperatura = 1 + max(0, (self.temperatura - 80) / 10)  # Aumento a partir de 80°C
        fator_corrente = 1 + max(0, (self.corrente - 2) / 0.5)        # Aumento a partir de 2A
        fator_vibracao = 1 + max(0, (self.vibracao - 5) / 2)          # Aumento a partir de 5 mm/s²

        # Calculando a vida útil com base nos fatores
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
        # A chance total de falha é calculada considerando a menor vida útil entre os motores
        if menor_tempo_falha < 0:
            return "Chance de falha do braço: 100.00%"
        elif menor_tempo_falha < 1:
            return "Chance de falha do braço: 100.00%"
        else:
            chance_falha_braco = max(0, (250 - menor_tempo_falha) / 250 * 100)
            return f"Chance de falha do braço: {chance_falha_braco:.2f}%"

    def prever_falhas(self):
        # Prever falhas para cada motor
        previsoes = [motor.previsao_falha() for motor in self.motores]
        return previsoes

def previsao(dia: str = '08', mes: str = '10', ano: str = '2024', msg_auto: bool = False):
    if msg_auto:
        comando = """
        SELECT 
            temperatura,
            corrente,
            vibracao_base,
            vibracao_braco
        FROM 
            dados
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
            DATE(data_registro) = '{ano}-{mes}-{dia}';
        """
    dados = consulta(comando)
    print(dados)
    temperatura, corrente, vibracao_base, vibracao_braco = dados[0]

    # Inicializar o braço robótico com os dados extraídos
    braco = BracoRobotico(temperatura, corrente, [vibracao_base, vibracao_braco])

    # Prever falhas para cada motor e imprimir
    previsoes = braco.prever_falhas()
    return braco.calcular_chance_total_falha(), previsoes

def meses():
    return consulta("SELECT DISTINCT strftime('%m', data_registro) AS mes FROM dados WHERE data_registro IS NOT NULL ORDER BY mes;")
