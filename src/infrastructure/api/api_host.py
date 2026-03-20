import os
import sys
from fastapi import FastAPI, HTTPException

# ESTO ES CLAVE: Permite que la API encuentre la carpeta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from src.application.ver_catalogo import VerCatalogo
from src.application.procesar_compra import ProcesarCompra
from src.infrastructure.persistence.supabase_libro_repo import SupabaseLibroRepository
from src.infrastructure.persistence.supabase_compra_repo import SupabaseCompraRepository

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

app = FastAPI(title="API Librería Hexagonal")

libro_repo = SupabaseLibroRepository(SUPABASE_URL, SUPABASE_KEY)
compra_repo = SupabaseCompraRepository(SUPABASE_URL, SUPABASE_KEY)

# Servicios (Casos de Uso)
cat_service = VerCatalogo(libro_repo)
compra_service = ProcesarCompra(libro_repo, compra_repo)

# --- ENDPOINTS ---

@app.get("/libros")
def listar_libros():
    """Endpoint para ver el catálogo"""
    return cat_service.ejecutar()

@app.post("/comprar")
def realizar_compra(cliente: str, libro_id: int, cantidad: int):
    """Endpoint para comprar (Simulando el flujo de la UI)"""
    try:
        # Creamos el formato de carrito que espera tu servicio
        carrito_simulado = [{"id": libro_id, "cantidad": cantidad}]
        resultado = compra_service.ejecutar(cliente, carrito_simulado)
        return {"mensaje": "Compra exitosa", "detalle": resultado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))