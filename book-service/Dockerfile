FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --no-cache

# Expose the port
EXPOSE 8082

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "8082", "--host", "0.0.0.0"]
