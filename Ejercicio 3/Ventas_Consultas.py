import mysql.connector
from mysql.connector import Error

def reporte_detallado():
    try:
        conexion = mysql.connector.connect(
            host='localhost', user='root', password='', database='ventas'
        )
        cursor = conexion.cursor()

        cursor.execute('''
            SELECT v.id, v.fecha, c.nombre, p.nombre, v.cantidad, v.total
            FROM ventas v
            INNER JOIN clientes c ON v.cliente_id = c.id
            INNER JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha DESC
        ''')
        filas = cursor.fetchall()

        print('\n===== HISTORIAL DE VENTAS =====')
        print(f"{'ID':<4} {'FECHA':<18} {'CLIENTE':<15} {'PRODUCTO':<18} {'CANT':<5} {'TOTAL':>10}")
        print('-' * 75)
        for f in filas:
            fecha_str = f[1].strftime('%Y-%m-%d %H:%M')
            print(f'{f[0]:<4} {fecha_str:<18} {f[2]:<15} {f[3]:<18} {f[4]:<5} ${float(f[5]):>9,.0f}')
            
    except Error as e:
        print(f"Error en consulta: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

reporte_detallado()