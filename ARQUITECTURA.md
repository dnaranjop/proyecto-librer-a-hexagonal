# ARQUITECTURA DEL SISTEMA: Diseño Hexagonal

## Descripción del Diseño
Se ha implementado un patrón de **Arquitectura Hexagonal (Ports & Adapters)** para desacoplar las reglas de negocio de la tecnología externa.

### 1. Núcleo (Dominio)
Ubicado en `src/domain/`. Es el corazón del sistema.
- **Entidades:** `Libro` y `Compra` usan **Pydantic** para asegurar la integridad de los datos.
- **Puertos (Interfaces):** `LibroRepository` define el contrato de qué puede hacer el sistema sin decir cómo se guarda.

### 2. Capa de Infraestructura (Adaptadores)
- **UI:** Streamlit (Capa externa que consume el dominio).
- **Persistencia:** (Fase 3) Implementará los puertos de salida para conectar con Supabase.

### 3. Verificación de Pureza
Se utiliza un script de análisis estático para asegurar que el **Dominio no importe librerías externas**. Actualmente, el sistema reporta **0 violaciones arquitectónicas**.

## Flujo de Datos
La interfaz de usuario envía datos a los Puertos del Dominio, los cuales son procesados por las Entidades. La respuesta vuelve a la UI sin que el Dominio sepa que existe una interfaz web.