# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 2000 available to the world outside this container
EXPOSE 2000

# Define environment variable
ENV DATABASE_URL /dev.sqlite
ENV TEST_DATABASE_URL /test.sqlite

# Run run.py when the container launches
CMD ["python", "run.py"]