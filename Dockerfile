# Use the official Python image
FROM python:3.11-slim

# Install necessary system dependencies (PostgreSQL client is optional for some use cases)
RUN apt-get update && apt-get install -y \
    pkg-config \
    build-essential \
    libpq-dev \
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

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app will run on
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn swiftnote.wsgi:application --bind 0.0.0.0:8000"]

