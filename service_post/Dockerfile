FROM python:3.11-slim

WORKDIR /app

COPY service_post/app.py /app/
COPY models_shared /app/models_shared
COPY scripts/wait-for-it.sh /app/scripts/wait-for-it.sh

RUN pip install flask sqlalchemy psycopg2-binary

EXPOSE 5002

CMD ["/app/scripts/wait-for-it.sh", "db:5432", "--", "python", "app.py"]
