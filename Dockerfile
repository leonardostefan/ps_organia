# Use uma imagem oficial do Python como base
FROM python:3.12

# Copie todas as dependências necessárias para a pasta /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copie o código-fonte da aplicação para a pasta /app
COPY ./app /app

# Defina o diretório de trabalho dentro do container como /app
WORKDIR /app

# Defina a porta que será usada pelo servidor FastAPI
EXPOSE 8000

# Inicie o servidor FastAPI ao iniciar o container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]