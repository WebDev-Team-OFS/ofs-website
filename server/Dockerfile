# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose port 8080 for the Flask app
EXPOSE 8080

# Run the database setup script and start the Flask app
CMD ["bash", "-c", "python create_database.py && python main.py"]