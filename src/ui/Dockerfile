FROM nvcr.io/nvidia/l4t-base:35.4.1
WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip python3-venv && \
    python3 -m pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /var/lib/apt/lists/*
COPY src /app/src
COPY docs /app/docs
ENV PYTHONPATH=/app/src
CMD ["python3", "-m", "ui.app"]
