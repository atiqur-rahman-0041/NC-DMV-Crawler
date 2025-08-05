FROM seleniarm/standalone-chromium:latest

USER root

# Install Python and venv
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set up venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies inside venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Run using venv's Python
CMD ["bash", "-c", "while true; do python crawler.py || echo 'Error $?'; sleep 60; done"]
