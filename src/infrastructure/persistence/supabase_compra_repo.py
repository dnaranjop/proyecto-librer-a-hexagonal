from supabase import create_client, Client
from src.domain.repositories import CompraRepository

class SupabaseCompraRepository(CompraRepository):
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def guardar(self, compra):
        # 1. Preparar la fecha como texto
        fecha_texto = compra.fecha.isoformat() if hasattr(compra.fecha, 'isoformat') else str(compra.fecha)

        # 2. Insertar la compra (Maestro)
        compra_dict = {
            "usuario_nombre": compra.usuario_nombre,
            "total": compra.total,
            "fecha": fecha_texto
        }
        
        res_compra = self.supabase.table("compras").insert(compra_dict).execute()
        
        # 3. Obtener el ID generado
        compra_id = res_compra.data[0]['id']
        compra.id = compra_id

        # 4. Preparar y guardar los items (Detalle)
        items_para_insertar = []
        for item in compra.items:
            items_para_insertar.append({
                "compra_id": compra_id,
                "libro_id": item.libro_id,
                "titulo": item.titulo,
                "cantidad": item.cantidad,
                "precio_unitario": item.precio_unitario
            })
        
        if items_para_insertar:
            self.supabase.table("items_compra").insert(items_para_insertar).execute()
        
        return compra
        return compra

    # --- IMPLEMENTACIÓN DE LOS MÉTODOS QUE FALTABAN (EL CONTRATO) ---

    def obtener_todas(self):
        response = self.supabase.table("compras").select("*").execute()
        return response.data

    def obtener_por_id(self, compra_id):
        response = self.supabase.table("compras").select("*").eq("id", compra_id).execute()
        return response.data[0] if response.data else None

    def obtener_por_usuario(self, nombre_usuario):
        response = self.supabase.table("compras").select("*").eq("usuario_nombre", nombre_usuario).execute()
        return response.data

    def contar_total_ventas(self):
        response = self.supabase.table("compras").select("id", count="exact").execute()
        return response.count if response.count else 0