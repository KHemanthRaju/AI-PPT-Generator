FROM python:3.9-slim

WORKDIR /app

COPY requirements_new.txt .
RUN pip install -r requirements_new.txt

COPY backend_api.py .

EXPOSE 8000

CMD ["uvicorn", "backend_api:app", "--host", "0.0.0.0", "--port", "8000"]