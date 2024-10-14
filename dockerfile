# Usar a imagem oficial do Python como base
FROM python:3.8-slim

# Definir o diretório de trabalho na imagem
WORKDIR /app

# Copiar o arquivo de requisitos para instalar as dependências
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt || { echo 'Falha na instalação de dependências'; exit 1; }

# Copiar todos os arquivos e pastas da aplicação para o diretório de trabalho
COPY . .

# Expor a porta que a aplicação irá rodar
EXPOSE 5000 

# Comando para executar a aplicação
CMD ["python", "app.py"]  # Altere 'app.py' se seu arquivo principal for outro
