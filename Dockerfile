FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Step 1 — Pre-install Cython so it's ready
RUN pip install --no-cache-dir Cython

# Step 2 — Now install everything else
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "scripts/check_and_generate_hand_ranges.py"]