# Use an official Python slim image
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your project files to the container
COPY . /app

# Install Python dependencies
RUN pip install redis rq pymongo flask requests python-dotenv

# Set environment variables (these can also be passed at runtime)
ENV REDIS_URL=redis://:26XC9YvCErtUsaybooUFr4NgeMfDMLqz@redis-12438.c305.ap-south-1-1.ec2.redns.redis-cloud.com:12438/0
ENV MONGO_URI=mongodb+srv://guptaprabhav131:4ytWTSdShcIy4OVJ@cluster0.rr2p5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

# Default command to run the worker
CMD ["python", "worker.py"]