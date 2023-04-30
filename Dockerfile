# Base image
FROM python:3.8-slim-buster

# Copy the content of the root folder to the working directory in the container

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update Linux
RUN apt-get update \
    && apt-get -y install libpq-dev gcc cron

# Copy cron file to the container
COPY cron /etc/cron.d/cron

# Give the permission
RUN chmod 0644 /etc/cron.d/cron

# Add the cron job
RUN crontab /etc/cron.d/cron

# Link cron log file to stdout
# RUN ln -s /dev/stdout /var/log/cron

# Instalar dependencias
COPY . /app
RUN mv .env.docker .env \
    && pip install -r requirements.txt

# Run the cron service in the foreground
CMD [ "cron", "-l", "2", "-f" ]
