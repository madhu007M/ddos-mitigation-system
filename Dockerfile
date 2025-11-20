FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose dashboard port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the dashboard
CMD ["python", "src/dashboard/app.py", "--host", "0.0.0.0", "--port", "5000"]
