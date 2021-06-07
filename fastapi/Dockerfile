FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy app
COPY . /app