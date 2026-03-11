from src.domain.repositories import LibroRepository

class VerCatalogo:
    def __init__(self, libro_repo: LibroRepository):
        self.libro_repo = libro_repo

    def ejecutar(self):
        return self.libro_repo.obtener_todos()