from supabase import create_client, Client
from src.domain.libro import Libro
from src.domain.repositories import LibroRepository

class SupabaseLibroRepository(LibroRepository):
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def obtener_todos(self):
        response = self.supabase.table("libros").select("*").execute()
        return [Libro(**row) for row in response.data]

    def obtener_por_id(self, libro_id):
        response = self.supabase.table("libros").select("*").eq("id", libro_id).execute()
        if response.data:
            return Libro(**response.data[0])
        return None

    # --- ESTOS SON LOS MÉTODOS QUE FALTABAN ---

    def obtener_por_categoria(self, categoria):
        response = self.supabase.table("libros").select("*").eq("categoria", categoria).execute()
        return [Libro(**row) for row in response.data]

    def guardar(self, libro):
        # Este método es por si quieres añadir libros nuevos desde la app
        libro_data = {
            "titulo": libro.titulo,
            "autor": libro.autor,
            "precio": libro.precio,
            "stock": libro.stock,
            "categoria": libro.categoria
        }
        self.supabase.table("libros").insert(libro_data).execute()

    def actualizar_stock(self, libro_id, nuevo_stock):
        self.supabase.table("libros").update({"stock": nuevo_stock}).eq("id", libro_id).execute()