# Usa a imagem oficial do Python 3.11
FROM python:3.11
RUN apt-get update && apt-get install -y ffmpeg

# Define o diretório de trabalho
WORKDIR /code

# Copia o arquivo de dependências
COPY ./requirements.txt /code/requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia toda a estrutura do projeto para dentro do contêiner
COPY . /code

# Expõe a porta 80
EXPOSE 80

# Executa o servidor Uvicorn
CMD ["python", "-m", "uvicorn", "Controller.main:app", "--host", "0.0.0.0", "--port", "80"]
