# Base image
FROM python:3.11-slim-buster

# Copy the content of the root folder to the working directory in the container
COPY . /app
WORKDIR /app

# Install required packages
RUN pip install -r requirements.txt

# Create cron job to run main script everyday at 7am
RUN echo "0 7 * * * python /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron
RUN chmod 0644 /etc/cron.d/my-cron
RUN touch /var/log/cron.log

# Start cron service
CMD cron && tail -f /var/log/cron.log