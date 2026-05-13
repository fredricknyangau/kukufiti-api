FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies PostgreSQL needs
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first — Docker caches this layer
# If requirements.txt doesn't change, this layer isn't rebuilt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

EXPOSE 8000

# Health check — Docker uses this to know if the container is ready
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]