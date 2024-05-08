# Use the official Python image from Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn==22.0.0
# Copy the current directory contents into the container at /app
COPY . .

# Specify the command to run your Flask application using Gunicorn
CMD ["gunicorn", "umlstudio:app", "-b", "0.0.0.0:5000"]
