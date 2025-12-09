FROM python:3.11-slim

WORKDIR /app

COPY ../../models_shared ./models_shared
COPY . .

RUN pip install flask sqlalchemy psycopg2-binary

CMD ["python", "app.py"]
