FROM python:3.12-slim

WORKDIR /app

COPY main.py .

RUN pip install --no-cache-dir flask

EXPOSE 8099

CMD ["python", "main.py"]
