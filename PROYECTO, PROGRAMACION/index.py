from PrestamoEstudiante import PrestamoEstudiante
from PrestamoDocente import PrestamoDocente
from conexion import obtener_conexion
from tabulate import tabulate

class Index:
    def menu(self):
        opcion = ""
        while opcion != "4":
            print("\n=== SISTEMA DE PRESTAMOS KANI I.A.N.V ===")
            print("1. Registrar nuevo prestamo")
            print("2. Registrar devolucion de libro")
            print("3. Ver todos los prestamos")
            print("4. Salir")

            opcion = input("Seleccione una opcion: ")

            if opcion == "1":
                print("\n--- NUEVO PRESTAMO ---")
                usuario = input("Nombre del usuario: ")
                tipo = input("Tipo de usuario (1: Estudiante / 2: Docente): ")
                titulo = input("Titulo del libro: ")
                categoria = input("Categoria del libro: ")

                tipo_usuario_str = "Estudiante" if tipo == "1" else "Docente"

                conexion = obtener_conexion()
                if conexion:
                    cursor = conexion.cursor()
                    query = """
                        INSERT INTO Prestamos (titulo, categoria, usuario, tipo_usuario, dias_retraso, multa)
                        VALUES (?, ?, ?, ?, 0, 0)
                    """
                    cursor.execute(query, (titulo, categoria, usuario, tipo_usuario_str))
                    conexion.commit()
                    conexion.close()
                    print(f"\n¡Libro '{titulo}' prestado con exito a {usuario}!")

            elif opcion == "2":
                print("\n--- REGISTRAR DEVOLUCION ---")
                usuario_buscar = input("Ingrese el nombre del usuario que devuelve el libro: ")

                conexion = obtener_conexion()
                if conexion:
                    cursor = conexion.cursor()
                    # Buscar prestamos a nombre de ese usuario
                    cursor.execute("SELECT id_prestamo, titulo, categoria, tipo_usuario FROM Prestamos WHERE usuario = ?", (usuario_buscar,))
                    registros = cursor.fetchall()

                    if not registros:
                        print(f"No se encontraron prestamos registrados a nombre de '{usuario_buscar}'.")
                    else:
                        print(f"\nPrestamos encontrados para {usuario_buscar}:")
                        for r in registros:
                            print(f"ID: {r[0]} | Libro: {r[1]} | Categoria: {r[2]} | Tipo: {r[3]}")
                        
                        id_prestamo = input("\nIngrese el ID del libro que esta devolviendo: ")
                        dias_retraso = int(input("¿Cuantos dias de retraso tuvo en la entrega?: "))

                        # Obtener los datos del préstamo seleccionado para calcular la multa
                        cursor.execute("SELECT titulo, categoria, tipo_usuario FROM Prestamos WHERE id_prestamo = ?", (id_prestamo,))
                        datos_prestamo = cursor.fetchone()

                        if datos_prestamo:
                            titulo, categoria, tipo_usuario = datos_prestamo

                            # Instancia de la clase correspondiente según la POO
                            if tipo_usuario == "Estudiante":
                                p = PrestamoEstudiante(titulo, categoria, usuario_buscar, dias_retraso)
                            else:
                                p = PrestamoDocente(titulo, categoria, usuario_buscar, dias_retraso)

                            multa = p.calcular_multa()

                            # Actualizar el registro en SQL Server
                            update_query = """
                                UPDATE Prestamos 
                                SET dias_retraso = ?, multa = ? 
                                WHERE id_prestamo = ?
                            """
                            cursor.execute(update_query, (dias_retraso, multa, id_prestamo))
                            conexion.commit()
                            print(f"\n¡Devolucion registrada! Multa calculada para {usuario_buscar}: ${multa:,.0f} COP")
                        else:
                            print("El ID ingresado no coincide.")
                    
                    conexion.close()

            elif opcion == "3":
                print("\n--- LISTA DE PRESTAMOS EN BASE DE DATOS ---")
                conexion = obtener_conexion()
                if conexion:
                    cursor = conexion.cursor()
                    cursor.execute("SELECT id_prestamo, usuario, tipo_usuario, titulo, dias_retraso, multa FROM Prestamos")
                    registros = cursor.fetchall()
                    conexion.close()

                    if not registros:
                        print("No hay prestamos registrados.")
                    else:
                        encabezados = ["ID", "Usuario", "Tipo", "Libro", "Días Retraso", "Multa (COP)"]
                        datos_tabla = [
                            [p[0], p[1], p[2], p[3], p[4], f"${p[5]:,.0f}"]
                            for p in registros
                        ]
                        print("\n" + tabulate(datos_tabla, headers=encabezados, tablefmt="grid"))
            elif opcion == "4":
                print("Saliendo del sistema...")

if __name__ == "__main__":
    app = Index()
    app.menu()