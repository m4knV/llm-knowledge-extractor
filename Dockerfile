FROM python:3.11-slim

# Label maintainer
LABEL maintainer="Nikos Makaritis <nikos.makaritis@gmail.com>"

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Make startup script executable
RUN chmod +x startup.sh

# CMD to run the application with migrations
CMD ["./startup.sh"]
