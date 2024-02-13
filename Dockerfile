# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.11

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /usr/src/app
COPY . /code

COPY ./requirements.txt /code/

# Update package lists and install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
