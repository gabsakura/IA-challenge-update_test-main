# ------------- Importações --------------
import google.generativeai as genai
from IA_folder.AI_functions import consulta, previsao, meses
from IA_folder.AI_specs import system_instruction
from functools import lru_cache
import numpy as np
import os
import time
import datetime
from dotenv import load_dotenv
# ----------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

GENERATION_CONFIG = {
    "temperature": 0.2, # Reduzido um pouco para a IA ser mais precisa ao escolher as funções
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
    "stop_sequences": ["Assistant:"],
}

SAFETY_SETTINGS = [
    {"category": cat, "threshold": "BLOCK_NONE"}
    for cat in [
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_DANGEROUS_CONTENT",
    ]
]

_chat_session = None


def _get_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError(
            "Chave da API Gemini não configurada. "
            "Defina GEMINI_API_KEY ou GOOGLE_API_KEY no arquivo .env"
        )
    return key


def _get_chat():
    global _chat_session
    if _chat_session is None:
        genai.configure(api_key=_get_api_key())
        
        # 1. Passamos as funções do Python no parâmetro 'tools'.
        # Isso dá à IA a habilidade de executar esses blocos de código diretamente no servidor.
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS,
            tools=[consulta, previsao, meses], 
            system_instruction=system_instruction
        )
        
        # 2. Ativamos o 'enable_automatic_function_calling=True'.
        # Agora, em vez de cuspir o texto da função, o Gemini executa a função no banco de dados,
        # recebe o retorno dos dados silenciosamente e formula a resposta final formatada para o usuário.
        # Removemos o INITIAL_PROMPT antigo que gerava respostas genéricas e conflitantes.
        _chat_session = model.start_chat(enable_automatic_function_calling=True)
        
    return _chat_session


def AI_request(user_input: str) -> str:
    print("\n=== Iniciando AI Request ===")
    print(f"Input recebido: {user_input[:100]}...")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resposta = _get_chat().send_message(user_input)
            texto = resposta.text.rstrip('\n')
            return texto
        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                raise e
            time.sleep((attempt + 1) * 1)


def AI_predict() -> str:
    prev = previsao(msg_auto=True)
    prompt = (
        f"Organize de forma concisa estas informações: {prev}. "
        "Traduza para o idioma atual da conversa. "
        "Se for a primeira mensagem, use português. "
        "Apresente apenas as informações essenciais."
    )
    return AI_request(prompt)


def AI_pdf(filtros, leituras):
    temperatura = np.mean(leituras["temperatura"]) if leituras.get("temperatura") else 0
    corrente = np.mean(leitures["corrente"]) if leituras.get("corrente") else 0
    vibracao_base = np.mean(leituras["vibracao_base"]) if leituras.get("vibracao_base") else 0
    vibracao_braco = np.mean(leituras["vibracao_braco"]) if leituras.get("vibracao_braco") else 0
    data_registro = leituras.get("timestamp", [])

    limites_ultrapassados = ""
    
    if isinstance(filtros, dict):
        time_range = filtros.get('timeRange', 'day')
        filter_day = filtros.get('day', datetime.date.today().strftime('%Y-%m-%d'))
        filter_month = filtros.get('month', '')
        filter_year = filtros.get('year', '2024')
    else:
        time_range = filtros
        filter_day = datetime.date.today().strftime('%Y-%m-%d')
        filter_month = ''
        filter_year = '2024'

    if time_range == "month" and data_registro:
        if len(data_registro[0]) >= 7:
            filter_month = data_registro[0][5:7]

    match time_range:
        case "day":
            filtros_label = "Diário"
            comando_sql = f"""
            SELECT strftime('%H:%M', data_registro) AS hora, 'temperatura' AS dado, temperatura AS valor
            FROM dados WHERE temperatura > 45 AND date(data_registro) = date('{filter_day}')
            UNION ALL
            SELECT strftime('%H:%M', data_registro) AS hora, 'corrente' AS dado, corrente AS valor
            FROM dados WHERE corrente > 5 AND date(data_registro) = date('{filter_day}')
            UNION ALL
            SELECT strftime('%H:%M', data_registro) AS hora, 'vibracao_base' AS dado, vibracao_base AS valor
            FROM dados WHERE vibracao_base > 5.5 AND date(data_registro) = date('{filter_day}')
            UNION ALL
            SELECT strftime('%H:%M', data_registro) AS hora, 'vibracao_braco' AS dado, vibracao_braco AS valor
            FROM dados WHERE vibracao_braco > 5.5 AND date(data_registro) = date('{filter_day}');
            """
            limites_ultrapassados = consulta(sql_=comando_sql)
        case "week":    
            filtros_label = "Semanal"
            data_ini = data_registro[0][:10] if data_registro else filter_day
            data_fim = data_registro[-1][:10] if data_registro else filter_day
            comando_sql = f"""
            SELECT DISTINCT strftime('%w', data_registro) AS dia_semana
            FROM dados WHERE (temperatura > 45 OR corrente > 5 OR vibracao_base > 5.5 OR vibracao_braco > 5.5)
            AND date(data_registro) BETWEEN date('{data_ini}') AND date('{data_fim}');
            """
            limites_ultrapassados = consulta(sql_=comando_sql)
        case "month":
            filtros_label = "Mensal"
            comando_sql = f"""
            SELECT DISTINCT strftime('%d', data_registro) AS dia
            FROM dados WHERE (temperatura > 60 OR corrente > 10 OR vibracao_base > 5 OR vibracao_braco > 5)
            AND strftime('%m', data_registro) = '{filter_month}';    
            """
            limites_ultrapassados = consulta(sql_=comando_sql)
        case "year":
            filtros_label = "Anual"
            comando_sql = f"""
            SELECT DISTINCT strftime('%m', data_registro) AS mes
            FROM dados WHERE (temperatura > 60 OR corrente > 10 OR vibracao_base > 5 OR vibracao_braco > 5)
            AND strftime('%Y', data_registro) = '{filter_year}';
            """
            limites_ultrapassados = consulta(sql_=comando_sql)
        case _:
            filtros_label = str(time_range)
            limites_ultrapassados = []
            
    input_IA = f"""Me crie um relátorio pdf com base nas seguintes informações, siga as instruções que estiverem entre '[]'.
    período de tempo analisado: {filtros_label}
    temperatura média: {temperatura:.2f}
    corrente média: {corrente:.2f}
    vibração média da base: {vibracao_base:.2f}
    vibração média do braço: {vibracao_braco:.2f}    
    quando os limites foram ultrapassado: {limites_ultrapassados}[Exiba como se eles tivessem sido solicitados pelo usuário]        
    """
    return AI_request(input_IA)