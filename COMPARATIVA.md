# COMPARATIVA: Monolito vs. Arquitectura Hexagonal

| Métrica | Monolito Original (Rama main) | Refactorización (Rama hexagonal) |
| :--- | :--- | :--- |
| **Líneas de Código (UI)** | ~50 (Mezclado con SQL) | ~20 (Limpio y agnóstico) |
| **Líneas de Código (Negocio)** | 0 (Inexistente) | ~150 (Dominio Puro con Pydantic) |
| **Tiempo de Ejecución Pruebas** | N/A (Manual/Dependiente de DB) | **~0.08s (20 pruebas en milisegundos)** |
| **Dependencias en el Core** | Supabase, Streamlit | **0 (Solo Python y Pydantic)** |
| **Acoplamiento** | Alto (Riesgo de fallos en cascada) | Bajo (Componentes intercambiables) |

### Observaciones
- La refactorización permitió alcanzar una **cobertura del 100% de reglas críticas** en el dominio.
- El tiempo de ejecución de pruebas bajó drásticamente al eliminar la dependencia de red (Supabase) mediante el uso de puertos.