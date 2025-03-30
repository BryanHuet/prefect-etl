FROM python:3.11-slim

# Installer les dépendances de base
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installer Prefect et Pandas
RUN pip install --no-cache-dir prefect pandas

# Définir le répertoire de travail
WORKDIR /app

# Exposer le port pour l'API de Prefect (si besoin)
EXPOSE 4200

# Définir la commande par défaut
CMD ["prefect", "version"]

