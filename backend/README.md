# 🚀 ¿Cómo crear una app de Django?

Este documento explica paso a paso cómo crear una aplicación utilizando **Django**, usando **Python**.

---

## ✅ Requisitos previos

- Tener instalado **Python**  
  👉 Recomendado: última versión estable desde [python.org](https://www.python.org/)

---

## 🎯 Creación de la app

👉 Documentación oficial: última versión estable desde [docs.djangoproject.com](https://docs.djangoproject.com/es/4.2/)

```bash
python -m venv menuEnv
```

- Primero creamos el entorno virtual para aislar las dependencias del proyecto.
- Activamos el entorno virtual según el sistema operativo:
  - **Windows:** `menuEnv\Scripts\activate`
  - **Linux/MacOS:** `source menuEnv/bin/activate`
- Instalamos Django con el siguiente comando:
  ```bash
  pip install django
  ```
- Creamos el proyecto Django:
  ```bash
  django-admin startproject menuBack
  ```
- Por defecto se usa SQLite como base de datos. Puedes modificar la configuración en `menuBack/settings.py`.
- Realizamos las migraciones iniciales:
  ```bash
  python manage.py migrate
  ```
- (Opcional) Creamos un superusuario para acceder al panel de administración:
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
- 📅 Fecha