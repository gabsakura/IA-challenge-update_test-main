FROM python:3.12-slim

WORKDIR /app

# Copiar os arquivos do projeto
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Criar diretório para o banco de dados
RUN mkdir -p instance && chmod 777 instance

# Expor a porta
EXPOSE 5001

# Definir variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Comando para iniciar a aplicação com mais logs
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--log-level", "debug", "--workers", "1", "--timeout", "120", "application:application"]
