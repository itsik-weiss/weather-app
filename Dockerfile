FROM python:3.9-slim

WORKDIR /app

# Define build argument for city name
ARG CITY_NAME=kuwait

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Set environment variable from build argument
ENV CITY_NAME=${CITY_NAME}

EXPOSE 3000

CMD ["python", "app.py"]
