FROM python:3.11-slim-bullseye

# Define build arguments
ARG API_PORT=8000

# Set environment variables (Docker Compose will override these)
ENV PYTHONUNBUFFERED=1 \
    DATABASE_URL=postgresql+psycopg2://postgres:mypassword@db:5432/mydatabase \
    API_PORT=${API_PORT}

# WORKDIR /ftc-user-service


# Copy only necessary files first (helps with Docker caching)
# COPY pyproject.toml poetry.lock README.md ./
COPY . .
# Install dependencies
RUN pip install poetry==1.8.3 && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# Copy the rest of the application
# COPY scripts/ /ftc-user-service/scripts/
# COPY src/ /ftc-user-service/src/

# Ensure scripts are executable
RUN chmod +x scripts/api.sh

# Expose the FastAPI port
EXPOSE ${API_PORT}

# Default command (override in Docker Compose if needed)
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
