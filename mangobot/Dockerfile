FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
  chromium-driver \
  && rm -rf /var/lib/apt/lists/*

# Copy application code to the container
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Run the app
CMD ["python", "-u", "run.py"]