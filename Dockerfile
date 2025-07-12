# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV/YOLO
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install system dependencies for OpenCV/YOLO

# Copy the rest of the application
COPY . .

# Expose ports
EXPOSE 8000
EXPOSE 5432

# Command to run the application
CMD ["dagster", "dev"]
