# Use the official Python image
FROM python:3.11-slim

# Install necessary system dependencies, including MariaDB client libraries
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Set environment variable for unbuffered output
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app into the container
COPY . .

# Copy the .env file into the container
COPY .env /app/.env

# Expose the port the app will run on
EXPOSE 8000

# Run the application
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
