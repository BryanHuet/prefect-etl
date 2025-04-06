# Use the official Python runtime image
FROM python:3.12.9-bookworm

# Installer les dépendances de base
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Create the app directory
RUN mkdir /app
WORKDIR /app

# Copy the Django project  and install dependencies
COPY requirements.txt  /app/

# run this command to install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the prefect port
EXPOSE 4200

CMD ["prefect", "server", "start", "--host", "0.0.0.0"]
