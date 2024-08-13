FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies, Google Chrome, and ChromeDriver
RUN apt-get update && \
  apt-get install -y wget gnupg && \
  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
  apt-get update && \
  apt-get install -y google-chrome-stable chromium-driver && \
  rm -rf /var/lib/apt/lists/*

# Copy application code to the container
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Run the app
CMD ["python", "-u", "run.py"]