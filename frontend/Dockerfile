FROM nginx:alpine

# Copiar archivos estáticos del frontend
COPY . /usr/share/nginx/html

# Configurar Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80