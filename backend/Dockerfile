# Usar imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer el puerto 5000 (Flask por defecto)
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python", "app.py"]