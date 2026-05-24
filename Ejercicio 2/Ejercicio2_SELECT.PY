import mysql.connector
from mysql.connector import Error

def obtener_estudiantes():
    try:
        conexion = mysql.connector.connect(
            host='localhost', user='root', password='', database='universidad'
        )
        cursor = conexion.cursor()
        
        cursor.execute('SELECT * FROM estudiantes ORDER BY apellido')
        filas = cursor.fetchall()
        
        if not filas:
            print('No hay estudiantes en la base de datos.')
            return

        print('=' * 70)
        print(f"{'ID':<5} {'NOMBRE':<15} {'APELLIDO':<15} {'CORREO':<22} {'PROM':>5}")
        print('=' * 70)
        for e in filas:
            print(f'{e[0]:<5} {e[1]:<15} {e[2]:<15} {e[3]:<22} {float(e[5]):>5.1f}')
        print('=' * 70)

    except Error as e:
        print(f"Error al consultar: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

obtener_estudiantes()