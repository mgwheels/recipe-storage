FROM python:3.14-slim

# Add uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock ./

# Install only dependencies (no project install, since app isn't packaged)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY ./app ./app

# Ensure /app is in Python path so app.main can be imported
ENV PYTHONPATH=/app

# Expose port and set CMD (matches your original uvicorn command, no --reload for prod)
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
