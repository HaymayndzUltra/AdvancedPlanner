FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copy only requirements first for better build caching
COPY data/pipelines/requirements.txt /workspace/data/pipelines/requirements.txt
RUN pip install --no-cache-dir -r /workspace/data/pipelines/requirements.txt

# Copy source and docs (schemas) referenced by pipeline and keep context minimal
COPY data/pipelines /workspace/data/pipelines
COPY docs/data/schemas /workspace/docs/data/schemas

# Default container runs a simple HTTP server so K8s liveness/readiness can succeed
EXPOSE 8080
CMD ["python", "-m", "http.server", "8080"]

