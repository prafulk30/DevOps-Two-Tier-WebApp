# Use an official Python runtime
FROM python:3.9-slim

# avoid interactive prompts during apt operations
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install system dependencies required for mysqlclient and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      gcc \
      default-libmysqlclient-dev \
      pkg-config \
      netcat \
      && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps first to leverage cache
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure wait-for-it is executable
RUN if [ -f ./wait-for-it.sh ]; then chmod +x ./wait-for-it.sh; fi

EXPOSE 5000

# Default command uses wait-for-it to wait for MySQL, then runs the app
CMD ["./wait-for-it.sh", "mysql:3306", "--", "python", "app.py"]
