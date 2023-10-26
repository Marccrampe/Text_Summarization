FROM python:3.8-slim-buster

WORKDIR /app

COPY ./src/summary-service.py ./
COPY ./requirements.txt  ./
COPY ./src/templates  ./templates
COPY ./src/static  ./static

RUN apt-get update && apt-get install -y enchant
RUN apt-get install -y myspell-fr-gut
RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "-w", "4", "summary-service:app", "--bind", "0.0.0.0:8000", "--timeout", "50000"]
