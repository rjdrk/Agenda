#!/usr/bin/env bash
set -e

echo "🚀 Iniciando aplicación Django..."
cd /code

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando conexión a la base de datos..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "   - Reintentando conexión a PostgreSQL..."
  sleep 2
done
echo "✅ Conexión a PostgreSQL exitosa!"

echo "📝 Creando y aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate --noinput

# Crear superusuario automáticamente (opcional)
echo "👤 Creando superusuario si no existe..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superusuario creado: admin/admin123')
else:
    print('ℹ️  Superusuario ya existe')
EOF

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🌟 ¡Aplicación lista! Accede a:"
echo "   🌐 Frontend: http://localhost:80"

# Usar DJANGO_ENV del .env
DJANGO_ENV=${DJANGO_ENV:-development}

if [ "$DJANGO_ENV" = "production" ]; then
    echo "Iniciando Django en producción con Gunicorn..."
    exec gunicorn app.wsgi:application --bind 0.0.0.0:8000
else
    echo "Iniciando Django en desarrollo con autoreload..."
    exec python manage.py runserver 0.0.0.0:8000
fi

# Iniciar servidor
exec "$@"
