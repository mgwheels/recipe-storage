FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY pyproject.toml uv.lock
RUN uv sync --frozen

# Copy application code
COPY ./app /app/app

# Expose port and set CMD
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
