# Dockerfile

# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first and install them
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port (choose 5000 or whatever your API Gateway uses)
EXPOSE 5000

# Run the API Gateway
CMD ["python", "api_gateway.py"]
