import mysql.connector
from mysql.connector import Error

def registrar_venta(cliente_id, producto_id, cantidad):
    try:
        conexion = mysql.connector.connect(
            host='localhost', user='root', password='', database='ventas'
        )
        cursor = conexion.cursor()

        # Iniciar la transacción de forma explícita
        conexion.start_transaction()

        # 1. Validar Stock
        cursor.execute('SELECT nombre, precio, stock FROM productos WHERE id = %s', (producto_id,))
        producto = cursor.fetchone()

        if not producto:
            raise ValueError('El producto no existe.')

        nombre_p, precio, stock_actual = producto

        if stock_actual < cantidad:
            raise ValueError(f'Stock insuficiente. Disponibles: {stock_actual}')

        # 2. Calcular e Insertar
        total = precio * cantidad
        cursor.execute('''
            INSERT INTO ventas (cantidad, total, cliente_id, producto_id) 
            VALUES (%s, %s, %s, %s)
        ''', (cantidad, total, cliente_id, producto_id))

        # 3. Descontar Inventario
        cursor.execute('UPDATE productos SET stock = stock - %s WHERE id = %s', (cantidad, producto_id))

        # Confirmar todo
        conexion.commit()
        print(f'¡Venta guardada con éxito! {cantidad}x {nombre_p} por un total de ${float(total):,.0f}')

    except (ValueError, Error) as e:
        if 'conexion' in locals() and conexion.is_connected():
            conexion.rollback() [cite: 75, 76]
        print(f'Transacción cancelada (Rollback). Razón: {e}') [cite: 75, 76]
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

# Prueba: El cliente 1 compra 2 unidades del producto 1
registrar_venta(cliente_id=1, producto_id=1, cantidad=2)