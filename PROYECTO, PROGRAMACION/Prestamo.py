from Libro import Libro
class Prestamo(Libro):
    def __init__(self, titulo, categoria, usuario, dias_retraso):
        super().__init__(titulo, categoria)
        self.usuario = usuario
        self.dias_retraso = dias_retraso
    def calcular_multa(self):
        return 0 