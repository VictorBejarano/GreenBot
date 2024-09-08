# Usar Nginx para servir archivos estáticos
FROM nginx:alpine
COPY . /usr/share/nginx/html

# Exponer el puerto 80
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]