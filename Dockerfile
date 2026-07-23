FROM python:3.11-slim

WORKDIR /app

# Copy requirements from backend directory
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
