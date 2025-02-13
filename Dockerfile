# Use the official Python 3.12 image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first (leveraging Docker cache)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
# Prevents buffering in logs
ENV PYTHONUNBUFFERED=1

# Expose the port Django runs on
EXPOSE 8001

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
