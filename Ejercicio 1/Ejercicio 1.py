import mysql.connector
from mysql.connector import Error

def crear_y_poblar_tienda():
    try:
        conexion = mysql.connector.connect(
            host='localhost', user='root', password='', database='tienda'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()

            # Crear tabla productos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(150) NOT NULL,
                    precio DECIMAL(10, 2) NOT NULL,
                    stock INT DEFAULT 0,
                    categoria VARCHAR(100)
                )
            ''')
            print('Tabla productos creada con éxito')

            # Insertar los 5 productos requeridos
            cursor.execute("SELECT COUNT(*) FROM productos")
            if cursor.fetchone()[0] == 0:
                sql = 'INSERT INTO productos (nombre, precio, stock, categoria) VALUES (%s, %s, %s, %s)'
                lista_productos = [
                    ('Laptop HP', 2500000, 10, 'Tecnologia'),
                    ('Mouse inalambrico', 85000, 50, 'Accesorios'),
                    ('Cuaderno universitario', 12000, 200, 'Papeleria'),
                    ('Audífonos Bluetooth', 320000, 25, 'Tecnologia'),
                    ('Mochila', 150000, 30, 'Accesorios')
                ]
                cursor.executemany(sql, lista_productos)
                conexion.commit()
                print('¡5 productos insertados exitosamente!')
            else:
                print('La tabla ya tiene datos registrados.')

    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

crear_y_poblar_tienda()