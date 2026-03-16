# 📚 Proyecto Librería: Arquitectura Hexagonal

Este proyecto demuestra la implementación de una Arquitectura Limpia (Hexagonal) para la gestión de una librería, permitiendo total independencia entre la lógica de negocio y las tecnologías de infraestructura.

---

## 🚀 Instalación Preliminar
Antes de ejecutar la aplicación, asegúrate de tener instaladas todas las librerías necesarias ejecutando el siguiente comando en tu terminal:

```bash
pip install -r requirements.txt

🛠️ Guía de Ejecución
El sistema cuenta con dos modos de persistencia intercambiables mediante la variable MODO_PRUEBA ubicada en el archivo src/infrastructure/ui/app.py:

1. Interfaz Web (Streamlit)
Para iniciar la aplicación visual de la librería:
Bash:
streamlit run src/infrastructure/ui/app.py
Modo Memoria (MODO_PRUEBA = True): Ideal para demostraciones rápidas. Los datos son volátiles y no requieren internet.

Modo Supabase (MODO_PRUEBA = False): Conecta con la base de datos PostgreSQL en la nube (Requiere credenciales configuradas y conexión a internet).

2. API REST (FastAPI)
Para habilitar el canal de comunicación para otros sistemas o realizar pruebas técnicas de los endpoints:
Bash:
python -m uvicorn src.infrastructure.api.api_host:app --reload
Documentación Interactiva: Una vez encendido el servidor, accede a http://127.0.0.1:8000/docs para probar los servicios mediante la interfaz de Swagger UI.

🏗️ Estructura del Proyecto
Siguiendo los principios de la Arquitectura Hexagonal, el código se organiza de la siguiente manera:

src/domain: Contiene las Entidades (modelos de datos) y los Puertos (interfaces de los repositorios). Es el núcleo puro del sistema.

src/application: Contiene los Casos de Uso (ej. Procesar Compra, Ver Catálogo) que orquestan la lógica de negocio.

src/infrastructure: Contiene los Adaptadores externos:

Persistencia: Implementaciones concretas de Repositorios (Supabase y Memoria).

UI: Interfaz de usuario interactiva desarrollada en Streamlit.

API: Adaptador de entrada para servicios REST mediante FastAPI.
