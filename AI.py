# ------------- Importações --------------
import google.generativeai as genai
from AI_folder.AI_functions import consulta, previsao, meses
from fpdf import FPDF
import AI_folder.AI_specs as AI_specs
# ----------------------------------------

GEMINI_API_KEY = "AIzaSyBow1PWoN12TuqSw7wudJP2NdAS0OcRYMo"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                              generation_config=AI_specs.generation_config,
                              system_instruction=AI_specs.system_instruction,
                              safety_settings=AI_specs.safety_settings,
                              tools = [consulta, previsao, meses])

AI = model.start_chat(enable_automatic_function_calling=True, history=[])

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

def criar_pdf(texto, imagem_cabecalho=None, nome_arquivo='relatorio.pdf', imagem_anexo=None):
    negrito = ['Relatório Técnico', '1. Identificação da Máquina', '2. Resumo Executivo', '3. Descrição Técnica da Máquina', '4. Histórico de Operação',
               '5. Procedimentos de Inspeção ou Manutenção', '6. Diagnóstico e Condição da Máquina', '7. Recomendações', '8. Conclusão']

    pdf = FPDF()
    pdf.add_page()

    # Adicionar imagem no topo centralizado
    if imagem_cabecalho:
        pdf.image(imagem_cabecalho, x=(pdf.w - 100) / 2, y=10, w=100)  # Ajuste a largura conforme necessário
        pdf.ln(8)  # Espaço abaixo da imagem (menor)

    # Configuração da fonte
    pdf.set_font("Arial", size=12)

    # Converter o texto para o encoding latin-1 
    texto = texto.encode('latin-1', 'replace').decode('latin-1')

    # Separar o texto em linhas e formatar negrito para os títulos
    linhas = texto.split('\n')
    for i, linha in enumerate(linhas):
        if linha in negrito:
            # Pular linha antes de cada título numerado, exceto o primeiro
            if i != 0:  # Verifica se não é o primeiro tópico
                pdf.ln(5)
            
            # Se for um título de ponto, colocar em negrito
            partes = linha.split(':')
            pdf.set_font("Arial", style='B', size=12)  # Negrito
            pdf.multi_cell(0, 10, partes[0] + ':')  # Título em negrito
            pdf.set_font("Arial", size=12)  # Texto normal
            pdf.multi_cell(0, 10, ':'.join(partes[1:]))  # Texto normal abaixo
            
            # Se a linha for "9. Anexos", adicionar a imagem do anexo
            if linha.startswith('Fotos e Imagens:') and imagem_anexo:
                pdf.ln(5)  # Pequeno espaço antes de adicionar a imagem
                pdf.image(imagem_anexo, x=(pdf.w - 100) / 2, w=100)  # Adiciona a imagem centralizada
                pdf.ln(5)  # Espaço abaixo da imagem
        else:
            pdf.multi_cell(0, 10, linha)

    # Gerar o arquivo PDF
    pdf.output(nome_arquivo)


def AI_pdf(user_input: str):
    r_pdf = AI.send_message(f"{user_input}")
    pdf_text = "\n" + r_pdf.text
    
    criar_pdf(texto=pdf_text, imagem_cabecalho="Logo.png", nome_arquivo="relatorio.pdf", imagem_anexo="AI/imagens/Foto.png")
    