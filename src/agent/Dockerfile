FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt -r /tmp/requirements-dev.txt
COPY src /app/src
COPY docs /app/docs
COPY README.md /app/README.md
COPY docs/placeholders.md /app/docs/placeholders.md
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "agent.main", "--dry-run"]
