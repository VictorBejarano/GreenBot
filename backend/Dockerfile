# Usar imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt requirements.txt

# Instalar las dependencias
RUN apt-get update && apt-get install -y \
    python3-dev \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar RPi.GPIO
RUN pip install RPi.GPIO

# Copiar el código fuente
COPY . .

# Exponer el puerto 5000 (Flask por defecto)
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python", "app.py"]