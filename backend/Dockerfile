# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files into the container
COPY . /app/
COPY ./Communication.py .

# Expose the port that your Flask app runs on
EXPOSE 5003

# Set the default command to execute when the container starts
CMD ["python", "Communication.py"]
