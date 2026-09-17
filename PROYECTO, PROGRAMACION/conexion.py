import pyodbc

def obtener_conexion():
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=.\\SQLEXPRESS07;'
            'DATABASE=Biblioteca KANI;'
            'Trusted_Connection=yes;'
            'TrustServerCertificate=yes;'
        )
        return conexion
    except Exception as e:
        print(f"Error al conectar a SQL Server: {e}")
        return None

if __name__ == "__main__":
    conn = obtener_conexion()
    if conn:
        print("¡Conexión exitosa a la base de datos Biblioteca KANI!")
        conn.close()