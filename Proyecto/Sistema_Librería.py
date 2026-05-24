import mysql.connector
from mysql.connector import Error

CONFIG = {
    'host': 'localhost', 'user': 'root', 'password': '', 'database': 'libreria_universitaria'
}

def registrar_venta():
    print('\n--- REGISTRAR COMPRA DE LIBRO ---')
    cliente_id = int(input('ID del Cliente: '))
    libro_id   = int(input('ID del Libro: '))
    cantidad   = int(input('Cantidad: '))

    try:
        con = mysql.connector.connect(**CONFIG)
        cur = con.cursor()
        con.start_transaction()

        # Verificar libro
        cur.execute('SELECT titulo, precio, stock FROM libros WHERE id = %s', (libro_id,))
        libro = cur.fetchone()
        if not libro: raise ValueError('El libro solicitado no existe.')

        titulo, precio, stock = libro
        if stock < cantidad: raise ValueError(f'Stock insuficiente. Solo quedan {stock} unidades.')

        # Guardar operación
        total = precio * cantidad
        cur.execute('INSERT INTO ventas (cantidad, total, cliente_id, libro_id) VALUES (%s, %s, %s, %s)',
                    (cantidad, total, cliente_id, libro_id))
        cur.execute('UPDATE libros SET stock = stock - %s WHERE id = %s', (cantidad, libro_id))
        
        con.commit()
        print(f'¡Venta exitosa! {cantidad} copia(s) de "{titulo}" procesada(s).')
    except (ValueError, Error) as e:
        if 'con' in locals() and con.is_connected(): con.rollback()
        print(f'Error al vender: {e}')
    finally:
        if 'con' in locals() and con.is_connected():
            cur.close(); con.close()

def reporte_mensual():
    print('\n--- GANANCIAS TOTALES POR MES ---')
    try:
        con = mysql.connector.connect(**CONFIG)
        cur = con.cursor()
        # Nota: Cambiamos strftime de SQLite por DATE_FORMAT de MySQL
        cur.execute('''
            SELECT DATE_FORMAT(fecha, '%Y-%m') AS mes, COUNT(*), SUM(total)
            FROM ventas
            GROUP BY mes
            ORDER BY mes DESC
        ''')
        for f in cur.fetchall():
            print(f"Mes: {f[0]} | Transacciones: {f[1]} | Total Vendido: ${float(f[2]):,.0f}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'con' in locals() and con.is_connected():
            cur.close(); con.close()

def menu():
    while True:
        print('\n===== BIENVENIDO A LA LIBRERÍA UNIVERSITARIA =====')
        print('1. Procesar venta de libro (Transacción)')
        print('2. Ver reporte de ingresos por mes')
        print('3. Salir del sistema')
        op = input('Elige una opción: ')
        if op == '1': registrar_venta()
        elif op == '2': reporte_mensual()
        elif op == '3': 
            print('¡Éxitos en tu entrega de librería universitaria!'); break
        else: print('Opción inválida.')

if __name__ == '__main__':
    menu()