from Prestamo import Prestamo
class PrestamoDocente(Prestamo):
    def calcular_multa(self):
        if self.dias_retraso > 0:
            return self.dias_retraso * 1000
        return 0