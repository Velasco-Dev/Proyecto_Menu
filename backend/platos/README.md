# 🚀 ¿Cómo crear una app de Django?

Este documento explica paso a paso cómo crear una aplicación utilizando **Django**, usando **Python**.

---

## ✅ Requisitos previos

- Tener instalado **Python**  
  👉 Recomendado: última versión estable desde [python.org](https://www.python.org/)

---

## 🎯 Creación de la app

👉 Documentación oficial: última versión estable desde [docs.djangoproject.com](https://docs.djangoproject.com/es/4.2/)

### 1. Crear y activar el entorno virtual

Desde la **carpeta raíz del proyecto**, ejecuta:

  ```bash
  python -m venv menuEnv
  ```

Para activar el entorno virtual, estando en la carpeta raíz, ejecuta (Según el sistema operativo):

  - **Windows:** `menuEnv\Scripts\activate`
  - **Linux/MacOS:** `source menuEnv/bin/activate`

### 2. Instalar dependencias

Dirígete al directorio del entorno virtual (`menuEnv`) y ejecuta:

  ```bash
  pip install django
  pip install djangorestframework
  pip install django-cors-headers
  ```
---

### 3. Crear el proyecto Django

  ```bash
  django-admin startproject menuBack
  ```

Por defecto se usa SQLite como base de datos. Puedes modificar la configuración en `menuBack/settings.py`.

### 3.1 Crear la app "platos"

Dentro del directorio del proyecto (`menuBack`) o el directorio `backend/`, ejecuta:

  ```bash
  python manage.py startapp platos
  ```

Esto generará la carpeta y archivos necesarios para la app "platos".

---

### 4. Migraciones

Dirígete al directorio `backend/` y ejecuta:

  ```bash
  python manage.py migrate
  ```

(Opcional) Para crear un superusuario:

  ```bash
  python manage.py createsuperuser
  ```

---

## 📁 Estructura y ejecución del proyecto

Una vez creada la app, debes dirigirte a la carpeta generada (por ejemplo, `menuBack`):

  ```bash
  cd menuBack
  ```

### ▶️ Para ejecutar la app:

Finalmente tenemos el proyecto creado y ejecutamos el servidor de desarrollo:

  ```bash
  python manage.py runserver
  ```

El servidor estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## ✍️ Autor

- Creado por Rubén Velasco (Velasco-Dev)
- 📅 Fecha de creación: 19/09/2025