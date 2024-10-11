# Usar uma imagem base do Python 3.9
FROM python:3.9-slim

# Instalar bash e outras dependências necessárias
RUN apt-get update && apt-get install -y bash

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de dependências (requirements.txt)
COPY requirements.txt ./

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o banco de dados para o contêiner
COPY dados.db ./


COPY modelo.pkl ./
# Copiar o restante do código da aplicação para o contêiner
COPY . .

# Expor a porta da API
EXPOSE 5000

# Comando para rodar a aplicação Python
CMD ["python", "app.py"]
