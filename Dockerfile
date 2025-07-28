FROM python:3.12

# Copie todas as dependências necessárias para a pasta /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --no-cache && \
    pip cache purge


# Copie o código-fonte da aplicação para a pasta /app
COPY ./app /app

# Defina o diretório de trabalho dentro do container como /app
WORKDIR /app

# Defina a porta que será usada pelo servidor FastAPI
EXPOSE 8000
ENV PYTHONPATH="${PYTHONPATH}:/app:/workspaces/ps_organia/app"

# Inicie o servidor FastAPI ao iniciar o container
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0"] # será definido via compose