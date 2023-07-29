# Use an official PostgreSQL image as the base image
FROM postgres:latest

# Environment variables for PostgreSQL database, user, and password
ENV POSTGRES_DB finance
ENV POSTGRES_USER finance
ENV POSTGRES_PASSWORD finance

# Environment variable for CONFIG_PATH
ENV CONFIG_PATH /app

# Copy the Python code and requirements to the container
#COPY ./data /app/data
#COPY ./main.py /app/main.py
#COPY ./wallet.py /app/wallet.py
#COPY ./requirements.txt /app/requirements.txt
#COPY ./config /app/config
COPY ./database/postgres_init.sql /docker-entrypoint-initdb.d/
#COPY ./database/* /app/database/

# Install required dependencies
RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && pip3 install --no-cache-dir --upgrade pip
#    && pip3 install --no-cache-dir -r /app/requirements.txt

# Expose PostgreSQL port
EXPOSE 5432

# Set the working directory
WORKDIR /app

# Run the Python script (you can replace "your_python_script.py" with the actual filename)
#CMD ["python3", "database/main.py"]
