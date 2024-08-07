FROM python:3.9

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt

COPY ./src /app
COPY ./data /app/data

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
