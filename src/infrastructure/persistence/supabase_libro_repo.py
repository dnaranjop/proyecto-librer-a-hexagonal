from supabase import create_client, Client
from src.domain.libro import Libro
from src.domain.repositories import LibroRepository

class SupabaseLibroRepository(LibroRepository):
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    # 1. Antes: obtener_por_id -> AHORA: buscar_libro_por_identificador
    def buscar_libro_por_identificador(self, libro_id):
        response = self.supabase.table("libros").select("*").eq("id", libro_id).execute()
        if response.data:
            return Libro(**response.data[0])
        return None

    # 2. Antes: obtener_todos -> AHORA: consultar_catalogo_completo
    def consultar_catalogo_completo(self):
        response = self.supabase.table("libros").select("*").execute()
        return [Libro(**row) for row in response.data]

    # 3. Antes: obtener_por_categoria -> AHORA: filtrar_libros_por_categoria
    def filtrar_libros_por_categoria(self, categoria):
        response = self.supabase.table("libros").select("*").eq("categoria", categoria).execute()
        return [Libro(**row) for row in response.data]

    # 4. Antes: guardar -> AHORA: registrar_nuevo_libro
    def registrar_nuevo_libro(self, libro):
        libro_data = {
            "titulo": libro.titulo,
            "autor": libro.autor,
            "precio": libro.precio,
            "stock": libro.stock,
            "categoria": libro.categoria
        }
        self.supabase.table("libros").insert(libro_data).execute()

    # 5. Antes: actualizar_stock -> AHORA: sincronizar_disponibilidad_stock
    def sincronizar_disponibilidad_stock(self, libro_id, nuevo_stock):
        self.supabase.table("libros").update({"stock": nuevo_stock}).eq("id", libro_id).execute()