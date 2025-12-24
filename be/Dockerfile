# Use official Python image
FROM python:3.13-slim

# Set workdir
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manager files
COPY requirements.txt ./

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY src/ ./src
COPY tests/ ./tests
COPY pytest.ini ./

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/test_db

# Run tests by default
CMD ["pytest", "tests", "-v", "--disable-warnings"]