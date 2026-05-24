import mysql.connector
from mysql.connector import Error

def crear_tablas_ventas():
    try:
        conexion = mysql.connector.connect(
            host='localhost', user='root', password='', database='ventas'
        )
        cursor = conexion.cursor()

        # 1. Tabla Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(150) UNIQUE NOT NULL,
                telefono VARCHAR(50),
                ciudad VARCHAR(100)
            )
        ''')

        # 2. Tabla Productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(150) NOT NULL,
                precio DECIMAL(10,2) NOT NULL,
                stock INT DEFAULT 0,
                categoria VARCHAR(100)
            )
        ''')

        # 3. Tabla Ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cantidad INT NOT NULL,
                total DECIMAL(10,2) NOT NULL,
                cliente_id INT NOT NULL,
                producto_id INT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')
        conexion.commit()
        print('Modelo relacional de ventas creado con éxito en XAMPP.')

        # Insertar unos datos base si está vacío para que hagas pruebas
        cursor.execute("SELECT COUNT(*) FROM clientes")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO clientes VALUES (NULL, 'Zahira Lopez', 'zahira@mail.com', '123456', 'Bogota')")
            cursor.execute("INSERT INTO productos VALUES (NULL, 'Teclado Mecánico', 180000, 20, 'Tecnologia')")
            conexion.commit()
            print('Datos de prueba iniciales agregados (Cliente ID: 1, Producto ID: 1).')

    except Error as e:
        print(f"Error al crear tablas: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

crear_tablas_ventas()