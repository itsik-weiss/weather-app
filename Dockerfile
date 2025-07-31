# Simple Dockerfile for weather app
FROM python:3.9-slim

WORKDIR /app

# Define build argument for city name
ARG CITY_NAME=kuwait

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variable from build argument
ENV CITY_NAME=${CITY_NAME}

# Expose the port the app runs on
EXPOSE 3000

# Run the application
CMD ["python", "app.py"]
