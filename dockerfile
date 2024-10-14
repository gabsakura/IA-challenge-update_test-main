FROM python:3.10-slim

# Atualizar pacotes do sistema e instalar dependências de build essenciais
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    && apt-get clean

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o requirements.txt
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos e pastas da aplicação para o diretório de trabalho
COPY . .

# Expor a porta (se necessário para aplicações web, como Flask)
EXPOSE 5001

# Comando para rodar a aplicação
CMD ["python", "app.py"]
