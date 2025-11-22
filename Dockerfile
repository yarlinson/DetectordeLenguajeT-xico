# Usar imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=toxic_detector.settings

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Crear directorio para archivos estáticos y base de datos
RUN mkdir -p /app/staticfiles && \
    mkdir -p /app/media

# Exponer puerto
EXPOSE 8000

# Script de inicio - crear en un directorio que no se sobrescriba
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'set -e' >> /entrypoint.sh && \
    echo 'cd /app' >> /entrypoint.sh && \
    echo 'echo "Aplicando migraciones..."' >> /entrypoint.sh && \
    echo 'python manage.py migrate --noinput' >> /entrypoint.sh && \
    echo 'echo "Recopilando archivos estáticos..."' >> /entrypoint.sh && \
    echo 'python manage.py collectstatic --noinput || true' >> /entrypoint.sh && \
    echo 'echo "Iniciando servidor Django..."' >> /entrypoint.sh && \
    echo 'exec python manage.py runserver 0.0.0.0:8000' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Usar el script de inicio
CMD ["/bin/bash", "/entrypoint.sh"]
