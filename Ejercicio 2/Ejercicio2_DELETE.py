import mysql.connector
from mysql.connector import Error

def eliminar_estudiante(id_estudiante):
    try:
        conexion = mysql.connector.connect(
            host='localhost', user='root', password='', database='universidad'
        )
        cursor = conexion.cursor()
        
        # Verificar si existe primero
        cursor.execute('SELECT nombre, apellido FROM estudiantes WHERE id = %s', (id_estudiante,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            print(f'Error: No existe ningún estudiante con ID {id_estudiante}')
            return
            
        confirmacion = input(f"¿Seguro que deseas eliminar a {resultado[0]} {resultado[1]}? (s/n): ")
        if confirmacion.lower() == 's':
            cursor.execute('DELETE FROM estudiantes WHERE id = %s', (id_estudiante,))
            conexion.commit()
            print('Estudiante eliminado correctamente.')
        else:
            print('Operación cancelada.')

    except Error as e:
        print(f"Error al eliminar: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

# Ejemplo de uso: intenta eliminar al estudiante con ID 3
eliminar_estudiante(3)