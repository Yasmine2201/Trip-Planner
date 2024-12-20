FROM python:3.11-slim

# Set work directory
WORKDIR /code

# Install dependencies
COPY ../back/requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY ../back /code/

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]