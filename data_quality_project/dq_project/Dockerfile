# Base image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=dq_project.settings \
    DEBUG=0 \
    SECRET_KEY=django-insecure-ehflpa^i$vc$$ixrxz%*2_ewkbe7c+i=muy*=5z0-5oro+ulrf\
    ALLOWED_HOSTS=localhost,127.0.0.1

ENV PYTHONPATH "${PYTHONPATH}:/Users/user/Desktop/projet_stage_text_mining/data_quality_project/dq_project/prediction"

RUN mkdir /app

# Set the working directory
WORKDIR /app

# Copy the Django project
COPY . .

COPY prediction/my_transformers.py /app
# COPY ./manage.py /app/

# Copy requirements and install dependencies
COPY ./requirements.txt requirements.txt


RUN pip install --upgrade pip

# Update package repositories
RUN apt-get update

# # Install Java
RUN apt-get install -y default-jdk


RUN pip install --no-cache-dir -r requirements.txt


# Expose port 8000
EXPOSE 8000

# Run the Django app
CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]
