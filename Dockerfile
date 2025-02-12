FROM ubuntu:latest

# Install uv and Python 3.12
RUN apt update && apt install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /root/.local/bin/uv python install 3.12 -v && \
    ls /root/.local/share/uv/python && \
    python3 -m venv /venv --python=3.12

# Set the working directory
WORKDIR /app

# Copy application files
COPY . .

# Activate virtual environment and install dependencies
RUN /venv/bin/pip install -r requirements.txt

# Set environment variables
ENV PATH="/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose the port Django runs on
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]