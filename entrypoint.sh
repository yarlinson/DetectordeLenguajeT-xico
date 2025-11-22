#!/bin/bash
set -e

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput || true

echo "Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000


