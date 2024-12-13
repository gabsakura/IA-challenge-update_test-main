FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Criar diretório instance se não existir
RUN mkdir -p instance

# Garantir permissões corretas
RUN chmod -R 777 instance

CMD gunicorn --bind 0.0.0.0:$PORT app:app
