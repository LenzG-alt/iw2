FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Instalar dependencias (se copia desde la raíz SGCP/)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto Django
COPY backend/MyDjangoProyect/ .

# Crear directorios para estáticos y medios
RUN mkdir -p staticfiles mediafiles

# Hacer ejecutable el entrypoint
COPY backend/entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]