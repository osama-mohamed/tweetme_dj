# Use the official Python image
FROM python:3.12.0-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app/src

# Copy the current directory contents into the container at /app
COPY /src .

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run Django commands
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD python manage.py runserver 0.0.0.0:8000