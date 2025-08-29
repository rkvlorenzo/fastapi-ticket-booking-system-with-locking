FROM python:3.12-slim

WORKDIR /src

COPY requirements.txt .
COPY alembic.ini .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app
COPY alembic/ ./alembic

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
