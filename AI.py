# ------------- Importações --------------
import google.generativeai as genai
from AI_folder.AI_functions import consulta, previsao, meses
from functools import lru_cache
import numpy as np
import os
import time
from dotenv import load_dotenv
# ----------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

GENERATION_CONFIG = {
    "temperature": 0.7,
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

INITIAL_PROMPT = """Você é um assistente eficiente e preciso. Siga estas diretrizes:
1. Forneça respostas diretas e concisas
2. Foque nos pontos principais da pergunta
3. Use linguagem clara e objetiva
4. Mantenha consistência nas respostas
5. Peça esclarecimentos quando necessário

Responda apenas quando solicitado através das funções do sistema."""

_chat_session = None


def _get_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError(
            "Chave da API Gemini não configurada. "
            "Defina GEMINI_API_KEY ou GOOGLE_API_KEY no arquivo .env (local) "
            "ou nas variáveis de ambiente do servidor."
        )
    return key


def _get_chat():
    global _chat_session
    if _chat_session is None:
        genai.configure(api_key=_get_api_key())
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS,
        )
        _chat_session = model.start_chat(
            history=[
                {"role": "user", "parts": [INITIAL_PROMPT]},
                {
                    "role": "model",
                    "parts": ["Entendido. Pronto para fornecer respostas eficientes."],
                },
            ]
        )
    return _chat_session

# Cache para respostas comuns
@lru_cache(maxsize=100)
def cached_AI_request(user_input: str) -> str:
    return AI_request_with_retry(user_input)

def AI_request_with_retry(user_input: str, max_retries: int = 3) -> str:
    print("\n=== Iniciando AI Request ===")
    print(f"Input recebido: {user_input[:100]}...")
    
    for attempt in range(max_retries):
        try:
            print(f"\nTentativa {attempt + 1} de {max_retries}")
            resposta = _get_chat().send_message(user_input)
            texto = resposta.text.rstrip('\n')
            print(f"Resposta obtida ({len(texto)} caracteres): {texto[:100]}...")
            return texto
            
        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                print("Todas as tentativas falharam")
                raise e
            print(f"Aguardando {(attempt + 1) * 1}s antes da próxima tentativa")
            time.sleep((attempt + 1) * 1)  # Backoff exponencial

def AI_request(user_input: str) -> str:
    # Verifica se a entrada é adequada para cache
    if len(user_input) < 1000:  # Cache apenas para entradas menores
        return cached_AI_request(user_input)
    return AI_request_with_retry(user_input)

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
    temperatura = np.mean(leituras["temperatura"])
    corrente = np.mean(leituras["corrente"])
    vibracao_base = np.mean(leituras["vibracao_base"])
    vibracao_braco = np.mean(leituras["vibracao_braco"])
    data_registro = leituras["timestamp"]

    limites_ultrapassados = ""
    
    match filtros:
        case "day":
            filtros = "Diário"
            comando_sql = f"""
            SELECT strftime('%H:%M', timestamp) AS hora, 'temperatura' AS dado, temperatura AS valor
            FROM leituras
            WHERE temperatura > 45 
            AND date(timestamp) = date({data_registro[0][:10]})
            UNION ALL
            SELECT strftime('%H:%M', timestamp) AS hora, 'corrente' AS dado, corrente AS valor
            FROM leituras
            WHERE corrente > 5
            AND date(timestamp) = date({data_registro[0][:10]})
            UNION ALL
            SELECT strftime('%H:%M', timestamp) AS hora, 'vibracao_base' AS dado, vibracao_base AS valor
            FROM leituras
            WHERE vibracao_base > 5.5
            AND date(timestamp) = date({data_registro[0][:10]})
            UNION ALL
            SELECT strftime('%H:%M', timestamp) AS hora, 'vibracao_braco' AS dado, vibracao_braco AS valor
            FROM leituras
            WHERE vibracao_braco > 5.5
            AND date(timestamp) = date({data_registro[0][:10]});
            """
            limites_ultrapassados = consulta(sql_ = comando_sql)
        case "week":    
            filtros = "Semanal"
            comando_sql = f"""
            SELECT DISTINCT strftime('%w', timestamp) AS dia_semana
            FROM leituras
            WHERE (temperatura > 45 OR corrente > 5 OR vibracao_base > 5.5 OR vibracao_braco > 5.5)
            AND date(timestamp) BETWEEN date({data_registro[0][:10]}) AND date({data_registro[-1][:10]});
            """
            limites_ultrapassados = consulta(sql_ = comando_sql)
        case "month":
            filtros = "Mensal"
            comando_sql = f"""
            SELECT DISTINCT strftime('%d', timestamp) AS dia
            FROM leituras
            WHERE (temperatura > 60 OR corrente > 10 OR vibracao_base > 5 OR vibracao_braco > 5)
            AND strftime('%m', timestamp) = {data_registro[0][6:8]};    
            """
            limites_ultrapassados = consulta(sql_ = comando_sql)
        case "year":
            filtros = "Anual"
            comando_sql = f"""
            SELECT DISTINCT strftime('%m', timestamp) AS mes
            FROM leituras
            WHERE (temperatura > 60 OR corrente > 10 OR vibracao_base > 5 OR vibracao_braco > 5)
            AND strftime('%Y', timestamp) = {data_registro[0][:5]};
            """
            limites_ultrapassados = consulta(comando_sql)
            
    input_IA = f"""Me crie um relátorio pdf com base nas seguintes informações, siga as instruções que estiverem entre '[]'.
    período de tempo analisado: {filtros}
    temperatura média: {temperatura}
    corrente média: {corrente}
    vibração média da base: {vibracao_base}
    vibração média do braço: {vibracao_braco}    
    quando os limites foram ultrapassado: {limites_ultrapassados}[Exiba como se eles tivessem sido solicitados pelo usuário]        
    """
    return AI_request(input_IA)
