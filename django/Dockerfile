FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy application code to the container
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Run the app
CMD ["python3", "-u", "run.py"]