# Usar imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Instalar git y otras dependencias necesarias
RUN apt-get update && apt-get install -y \
    git \
    python3-dev \
    gcc \
    libgpiod2 \
    libbluetooth-dev \
    bluetooth \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos necesarios
COPY requirements.txt requirements.txt

# Instalar dependencias desde requirements.txt
RUN pip install -r requirements.txt

# Instalar PyBluez desde el repositorio de GitHub
RUN pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez

# Instalar RPi.GPIO
RUN pip install RPi.GPIO

# Copiar el código fuente
COPY . .

# Exponer el puerto 5000 (Flask por defecto)
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python", "app.py"]