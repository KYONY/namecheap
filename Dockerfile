FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=on

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    netcat-traditional \
    curl \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pipenv

# Install Python dependencies
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --dev

# Copy project
COPY . .

# Copy and set up entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]