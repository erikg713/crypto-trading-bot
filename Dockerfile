# Base image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports if dashboard is enabled
EXPOSE 8501

# Run main script
CMD ["python", "src/main.py"]
