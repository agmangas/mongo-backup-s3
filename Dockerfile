FROM ubuntu:16.04

# Install Python
RUN apt-get update && \
    apt-get -y install python python-pip

# Install AWS CLI and schedule package
RUN pip install awscli schedule

# Install MongoDB tools
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
RUN echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | \
    tee /etc/apt/sources.list.d/mongodb-org-3.2.list
RUN apt-get update && \
    apt-get install -y mongodb-org-tools

# Add scripts
ADD scripts/backup.sh /app/backup.sh
ADD scripts/run.py /app/run.py
RUN chmod +x /app/backup.sh
RUN chmod +x /app/run.py

# Run the schedule command on startup
CMD ["python", "-u", "/app/run.py"]
