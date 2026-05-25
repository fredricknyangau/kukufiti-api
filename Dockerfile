#==============================================================================
# Stage 1: Builder — installs dependencies, compiles nothing to the final image
#==============================================================================
FROM python:3.12.2-slim-bookworm AS Builder

# Prevents Python from writing .pyc files — saves space in image
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout/stderr — logs appear immediately
ENV PYTHONUNBUFFERED=1

WORKDIR /build

# Install system dependencies - only needed at build time, not runtime
RUN apt-get update && apt-get install -y  --no-install-recommends\
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first — Docker caches this layer
# If requirements.txt doesn't change, this layer isn't rebuilt
COPY requirements.txt .

# Install into a prefix directory — easy to copy to final stage
RUN pip install --no-cache-dir  --prefix=/install -r requirements.txt

# ============================================================
# Stage 2: Runtime — minimal image, no build tools
# ============================================================
FROM python:3.12.2-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Runtime system dependencies only (libpq for asyncpg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user — never run production containers as root
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

# Set working directory inside the container
WORKDIR /app


# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Health check — Docker uses this to know if the container is ready
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose the application port
EXPOSE 8000

# Default entrypoint — overridden per service in docker-compose / K8s
CMD ["python", "-m", \
     "uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", "--reload"]