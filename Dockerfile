# ============ BUILDER STAGE ============
FROM python:3.12-slim AS builder

# Install uv via pip - simple and sufficient for this project
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy only dependency files first - maximizes Docker layer cache hits.
# uv sync only reruns when pyproject.toml/uv.lock change, not on every code edit.
COPY pyproject.toml uv.lock ./

# Install ONLY production dependencies (excludes the 'dev' group: pytest, httpx),
# exactly as pinned in uv.lock (--frozen = no re-resolution)
RUN uv sync --frozen --no-dev

# Now copy the rest of the application code
COPY . .


# ============ RUNTIME STAGE ============
FROM python:3.12-slim AS runtime

WORKDIR /app

# Create a dedicated non-root user - never run production containers as root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy only the built virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy only the application code needed at runtime
COPY --from=builder /app/app /app/app
COPY --from=builder /app/alembic /app/alembic
COPY --from=builder /app/alembic.ini /app/alembic.ini

# Ensure the venv's binaries (python, uvicorn) are what gets used
ENV PATH="/app/.venv/bin:$PATH"

# Drop privileges before running anything
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]