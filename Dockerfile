# Base image
FROM python:3.11.3-alpine

# Copy the content of the root folder to the working directory in the container

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update Linux
RUN apk update
#    apk add --virtual build-deps gcc python-dev musl-dev && \
#    apk add postgresql-dev && \

# Copy cron file to the container
COPY cron /etc/cron.d/cron

# Give the permission
RUN chmod 0644 /etc/cron.d/cron

# Add the cron job
RUN crontab /etc/cron.d/cron

# Link cron log file to stdout
RUN ln -s /dev/stdout /var/log/cron

# Instalar dependencias
COPY . /app
RUN pip install -r requirements.txt

# Run the cron service in the foreground
CMD [ "crond", "-l", "2", "-f" ]
