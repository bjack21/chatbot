FROM python:3.11-slim
WORKDIR /app

# Install build dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PORT=8000
EXPOSE 8000

# Use gunicorn for production-like server
CMD ["gunicorn", "web:app", "-b", "0.0.0.0:8000", "--workers", "1"]
