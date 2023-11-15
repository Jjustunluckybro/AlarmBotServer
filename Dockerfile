FROM python:3.11

RUN mkdir /NotionBackend

WORKDIR /NotionBackend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn src.app_main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000