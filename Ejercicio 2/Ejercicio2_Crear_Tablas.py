import mysql.connector
from mysql.connector import Error

def inicializar_estudiantes():
    try:
        # Conectarse a la base de datos que creaste en phpMyAdmin
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='universidad'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()

            # 1. Crear la tabla estudiantes con la estructura correcta para MySQL
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estudiantes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    correo VARCHAR(150) UNIQUE NOT NULL,
                    edad INT,
                    promedio DECIMAL(3, 1) DEFAULT 0.0
                )
            ''')
            print('¡Tabla "estudiantes" creada exitosamente en XAMPP!')

            # 2. Insertar datos de prueba iniciales si la tabla está vacía
            cursor.execute("SELECT COUNT(*) FROM estudiantes")
            if cursor.fetchone()[0] == 0:
                sql = '''INSERT INTO estudiantes (nombre, apellido, correo, edad, promedio) 
                         VALUES (%s, %s, %s, %s, %s)'''
                estudiantes_iniciales = [
                    ('Maria', 'Lopez', 'maria@uni.edu', 19, 4.2),
                    ('Carlos', 'Ramirez', 'carlos@uni.edu', 20, 3.8),
                    ('Ana', 'Torres', 'ana@uni.edu', 18, 4.7)
                ]
                cursor.executemany(sql, estudiantes_iniciales)
                conexion.commit()
                print('¡Estudiantes de prueba registrados con éxito!')
            else:
                print('La tabla ya contiene registros.')

    except Error as e:
        print(f"Error al inicializar: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

if __name__ == '__main__':
    inicializar_estudiantes()