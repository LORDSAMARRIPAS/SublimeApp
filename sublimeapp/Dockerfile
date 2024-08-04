# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Debug: Print the contents of requirements.txt to verify it's correct
RUN cat requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Debug: Verify that gunicorn is installed
RUN pip show gunicorn || echo "gunicorn not found"
RUN which gunicorn || echo "gunicorn executable not found"

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Run the collectstatic command to gather static files
RUN python manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sublimeapp.wsgi:application"]
