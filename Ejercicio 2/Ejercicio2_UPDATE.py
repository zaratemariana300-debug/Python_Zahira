import mysql.connector
from mysql.connector import Error

def actualizar_promedio(id_estudiante, nuevo_promedio):
    try:
        conexion = mysql.connector.connect(
            host='localhost', user='root', password='', database='universidad'
        )
        cursor = conexion.cursor()
        
        sql = 'UPDATE estudiantes SET promedio = %s WHERE id = %s'
        cursor.execute(sql, (nuevo_promedio, id_estudiante))
        conexion.commit()
        
        if cursor.rowcount > 0:
            print(f'¡Promedio actualizado para el estudiante ID {id_estudiante}!')
        else:
            print(f'No se encontró ningún estudiante con el ID {id_estudiante}.')

    except Error as e:
        print(f"Error al actualizar: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

# Ejemplo de uso: cambia el promedio del ID 1 a 4.8
actualizar_promedio(1, 4.8)