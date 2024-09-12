FROM python:3.11-slim

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create and set the working directory
WORKDIR /app

# Install the dependencies
RUN pip install --no-cache-dir squareup

# Copy the rest of the application code into the container at /app
COPY . /app/

# Expose the port Flask runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run"]