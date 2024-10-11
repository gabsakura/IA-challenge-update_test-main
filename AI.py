import google.generativeai as genai
from AI_functions import consulta, previsao
from time import sleep
import AI_specs


GEMINI_API_KEY = "AIzaSyBow1PWoN12TuqSw7wudJP2NdAS0OcRYMo"
genai.configure(api_key=GEMINI_API_KEY)


model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                              generation_config=AI_specs.generation_config,
                              system_instruction=AI_specs.system_instruction,
                              safety_settings=AI_specs.safety_settings,
                              tools = [consulta, previsao])

AI = model.start_chat(enable_automatic_function_calling=True, history=[])

def AI_request(user_input: str) -> str:
    resposta = AI.send_message(user_input)
    texto_resposta = resposta.text

    if '\n' in texto_resposta:
        texto_resposta = texto_resposta.rstrip('\n')

    return texto_resposta


def AI_predict() -> str:
    while True:
        sleep(300)
        prev = previsao(msg_auto=True)

        resposta = AI.send_message(
            f"Organize essa lista, {prev} como se fosse ela tivesse sido retornada pela função previsão para o dia de hoje, "
            f"caso esteja vazia, diga ao usuário que não exixtem dados para o dia solicitado."
            f"Caso seja o dia atual responda que não existem dados pra o dia de hoje."
            f"Sempre ao responder, responda no idioma atual da conversa")

        texto_resposta = resposta.text
        if '\n' in texto_resposta:
            texto_resposta = texto_resposta.rstrip('\n')

        return texto_resposta