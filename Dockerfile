# Use the official Python 3.11 image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/mango

# Install any needed packages specified in requirements.txt and create database
COPY . .

RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

ARG PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "-u", "app.py"]