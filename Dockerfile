# Base image
FROM python:3.11-slim-bullseye

# Copy the content of the root folder to the working directory in the container

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install required packages
RUN apt-get update && apt-get install -y libpq-dev gcc && pip install psycopg2
RUN apt-get install -y cron && cron

COPY . /app
RUN pip install -r requirements.txt


# Create cron job to run main script everyday at 7am
# Add the cron job
RUN echo "0 7 * * * python /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron
RUN chmod 0644 /etc/cron.d/my-cron
RUN touch /var/log/cron.log

# Start cron service
CMD cron && tail -f /var/log/cron.log