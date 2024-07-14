# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/sublime

# Install dependencies
COPY /requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY sublimeapp/ .

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]