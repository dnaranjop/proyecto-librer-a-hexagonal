# ARQUITECTURA DEL SISTEMA: Diseño Hexagonal (Fase 4 Finalizada)

## Descripción del Diseño
Se ha implementado un patrón de **Arquitectura Hexagonal (Ports & Adapters)** para desacoplar totalmente las reglas de negocio de la tecnología externa, permitiendo que el sistema evolucione sin riesgo.

### 1. Núcleo (Dominio y Aplicación)
Ubicado en `src/domain/` y `src/application/`. Es el corazón del sistema:
* **Entidades:** `Libro` y `Compra` (modelos puros con Pydantic).
* **Puertos (Interfaces):** `LibroRepository` y `CompraRepository`. Definen el contrato de persistencia.
* **Casos de Uso (Capa de Aplicación):** `VerCatalogo` y `ProcesarCompra`. Orquestan la lógica sin depender de quién los llame.

### 2. Capa de Infraestructura (Adaptadores de Entrada y Salida)
El sistema ahora soporta múltiples tecnologías gracias a su diseño modular:

* **Adaptadores de Entrada (Inbound):**
    * **UI Web:** Desarrollada en **Streamlit** para interacción humana.
    * **API REST:** Desarrollada en **FastAPI** para consumo de otros sistemas (Fase 4).
* **Adaptadores de Salida (Outbound):**
    * **Persistencia en Memoria:** Para pruebas unitarias de alta velocidad.
    * **Persistencia Supabase:** PostgreSQL en la nube para producción.

### 3. Verificación de Pureza
Se mantiene un script de análisis estático (`verificar_pureza.py`) que garantiza que el **Dominio no tenga dependencias de terceros**. El sistema reporta **0 violaciones arquitectónicas**, cumpliendo con la Regla de Dependencia de la Clean Architecture.

## Flujo de Datos
El flujo es ahora multidireccional en la entrada: Tanto la Web como la API envían datos a los mismos Casos de Uso. La respuesta vuelve al adaptador correspondiente sin que el Dominio sepa si fue invocado por un navegador o por una petición HTTP.