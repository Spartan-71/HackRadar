# Dockerfile
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 \
UV_SYSTEM_PYTHON=1


# Working Directory
WORKDIR /app


# Install system dependancies
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential libpq-dev curl \
&& rm -rf /var/lib/apt/lists/*

# Install yv (fast dependency manager)
RUN pip install uv

# Copy pyproject.toml
COPY pyproject.toml ./

# Install dependancies
RUN uv pip install -e .

# Copy project files
COPY . .

# Entrypoint script
RUN chmod +x docker/entrypoint.sh
ENTRYPOINT ["./docker/entrypoint.sh"]

# Expose FastAPI port
EXPOSE 8000

