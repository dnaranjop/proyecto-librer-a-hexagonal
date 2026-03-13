from src.domain.repositories import LibroRepository

class VerCatalogo:
    def __init__(self, libro_repo: LibroRepository):
        self.libro_repo = libro_repo

    def ejecutar(self):
        # CAMBIO: De obtener_todos() a consultar_catalogo_completo()
        return self.libro_repo.consultar_catalogo_completo()