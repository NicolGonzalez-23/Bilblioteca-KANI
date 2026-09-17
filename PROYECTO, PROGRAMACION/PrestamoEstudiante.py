from Prestamo import Prestamo
class PrestamoEstudiante(Prestamo):
    def calcular_multa(self):
        if self.dias_retraso > 0:
            return self.dias_retraso * 2000
        return 0