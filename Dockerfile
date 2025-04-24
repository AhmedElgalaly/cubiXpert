# Use the official Python image from the Docker Hub
FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# install dependencies first
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run the script
CMD ["python", "main.py"]
