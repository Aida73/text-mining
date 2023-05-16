# Base image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=dq_project.settings 

#ENV PYTHONPATH "${PYTHONPATH}:/Users/user/Desktop/projet_stage_text_mining/data_quality_project/dq_project/prediction"



RUN mkdir /app

# Set the working directory
WORKDIR /app
# copy entrypoint.sh
COPY ./entrypoint.sh entrypoint.sh
COPY prediction/my_transformers.py /app
COPY ./requirements.txt requirements.txt

#RUN sed -i 's/\r$//g' /app/entrypoint.sh

RUN chmod +x entrypoint.sh

# Copy the Django project
COPY . .
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get update
#RUN apt-get install -y apk-tools

#Install Java
RUN apt-get install -y default-jdk

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

# Run the Django app
#CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]
# run entrypoint.sh

