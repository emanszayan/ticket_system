# Use official Python image as base
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /ticket_system

# Copy only requirements.txt first (prevents re-installing dependencies on minor changes)
COPY requirements.txt /ticket_system/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project files
COPY . /ticket_system/

# Expose the default Django port
EXPOSE 8000

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py makemigrations && \
                 python manage.py migrate && \
                 python manage.py collectstatic --noinput && \
                 python manage.py runserver 0.0.0.0:8000"]
