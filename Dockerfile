# ============================================================================
# Multi-stage Dockerfile for Student Management System
# Supports runtime parameterization (Python 3.11 / 3.12) for Jenkins parallel builds
# ============================================================================

ARG PYTHON_VERSION=3.12

# ----------------------------------------------------------------------------
# Stage 1: Builder (Compile wheels & run unit tests)
# ----------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# ----------------------------------------------------------------------------
# Stage 2: Runtime (Lightweight production image without compiler tools)
# ----------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

ARG APP_VERSION=1.0.0
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_VERSION=${APP_VERSION} \
    APP_PORT=5000

WORKDIR /app

# Create a non-root user for container security
RUN useradd --create-home --shell /bin/bash appuser

# Copy pre-built wheels from builder stage and install them cleanly
COPY --from=builder /build/wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

# Copy application source code and test suite
COPY app/ ./app/
COPY tests/ ./tests/
COPY run.py .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "run:app"]