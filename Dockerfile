# Usa la imagen de Python 3.11
FROM python:3.11-slim

# Set environment variables
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false
# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos
COPY pyproject.toml poetry.lock* /app/

# Instala Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Regenerate poetry.lock to sync with pyproject.toml
RUN poetry lock --no-update

# Install all dependencies, including dev dependencies
RUN poetry install --with dev

# Copia el resto del código de la aplicación
COPY . /app

# Exponer el puerto que FastAPI usará
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

