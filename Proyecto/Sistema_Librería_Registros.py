import mysql.connector
from mysql.connector import Error

def preparar_libreria():
    try:
        conexion = mysql.connector.connect(
            host='localhost', user='root', password='', database='libreria_universitaria'
        )
        cursor = conexion.cursor()

        # Tablas de la librería
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS libros (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(150) NOT NULL,
                precio DECIMAL(10,2) NOT NULL,
                stock INT DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(150) UNIQUE NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cantidad INT NOT NULL,
                total DECIMAL(10,2) NOT NULL,
                cliente_id INT NOT NULL,
                libro_id INT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (libro_id) REFERENCES libros(id)
            )
        ''')
        conexion.commit()
        print("Estructura de la librería universitaria lista.")

        # Insertar catálogo inicial si está vacío
        cursor.execute("SELECT COUNT(*) FROM libros")
        if cursor.fetchone()[0] == 0:
            sql = "INSERT INTO libros (titulo, precio, stock) VALUES (%s, %s, %s)"
            libros_inicio = [
                ('Cálculo Integral', 85000, 15),
                ('Introducción a Python', 60000, 30),
                ('Bases de Datos Relacionales', 75000, 12)
            ]
            cursor.executemany(sql, libros_inicio)
            
            # Cliente inicial de prueba
            cursor.execute("INSERT INTO clientes VALUES (NULL, 'Estudiante Sena', 'sena@misena.edu.co')")
            conexion.commit()
            print("Catálogo de libros y cliente de prueba agregados con éxito.")

    except Error as e:
        print(f"Error en preparación: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

if __name__ == '__main__':
    preparar_libreria()