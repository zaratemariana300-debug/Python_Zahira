import mysql.connector
from mysql.connector import Error

def estadisticas_generales():
    try:
        conexion = mysql.connector.connect(
            host='localhost', user='root', password='', database='ventas'
        )
        cursor = conexion.cursor()

        print('\n===== REPORTE ESTADÍSTICO DE VENTAS =====')
        
        # Total global vendido
        cursor.execute('SELECT SUM(total) FROM ventas')
        total = cursor.fetchone()[0]
        print(f'Total Ingresos:       ${float(total or 0):>12,.0f}')

        # Agrupado por ciudad usando GROUP BY
        print('\n--- Ventas por Ciudad ---')
        cursor.execute('''
            SELECT c.ciudad, COUNT(v.id), SUM(v.total)
            FROM ventas v
            INNER JOIN clientes c ON v.cliente_id = c.id
            GROUP BY c.ciudad
        ''')
        for fila in cursor.fetchall():
            print(f'  {fila[0]:<15} ({fila[1]} ventas) -> Total: ${float(fila[2]):,.0f}')

    except Error as e:
        print(f"Error al generar estadísticas: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

estadisticas_generales()