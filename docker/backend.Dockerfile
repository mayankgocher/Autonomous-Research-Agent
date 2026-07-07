FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies (including SQLite if needed, though included in Python standard library)
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# Expose FastAPI port
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
