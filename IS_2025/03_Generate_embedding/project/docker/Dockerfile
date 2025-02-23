FROM python:3.12.4-slim-bookworm

WORKDIR /app

COPY app/. .
RUN apt-get update -y
RUN apt-get install -y libmariadb-dev
RUN apt install build-essential -y 
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "./app.py" ]
