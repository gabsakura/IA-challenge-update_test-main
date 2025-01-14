# ------------- Importações --------------
import google.generativeai as genai
from google.ai import generativelanguage as glm
from AI_folder.AI_functions import consulta, previsao, meses
from fpdf import FPDF
import AI_folder.AI_specs as AI_specs
import numpy as np
import os
# ----------------------------------------

# Configure API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Carrega a chave da API do arquivo .env
genai.configure(api_key=GEMINI_API_KEY)

# Define function declarations properly
function_declarations = [
    {
        "name": "consulta",
        "description": "Function to perform consultation",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to process"
                }
            },
            "required": ["query"]
        }
    }
]

# Initialize the model with proper tool configuration
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config={
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
)

# Start chat without tools for now
AI = model.start_chat(history=[])

def AI_request(user_input: str) -> str:
    resposta = AI.send_message(user_input)
    texto_resposta = resposta.text

    if '\n' in texto_resposta:
        texto_resposta = texto_resposta.rstrip('\n')

    return texto_resposta

def AI_predict() -> str:
    prev = previsao(msg_auto=True)

    resposta = AI.send_message(f"Organize essas informações {prev}. Traduza para a idioma atual da conversa."
                               f"Caso essa seja a primeira mensagem, escreva em português."
                               f"Ao responder a essa mensagem, apresente apenas as informações.")

    texto_resposta = resposta.text
    if '\n' in texto_resposta:
        texto_resposta = texto_resposta.rstrip('\n')

    return texto_resposta


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
