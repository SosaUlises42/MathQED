import bcrypt
from models.databasemodel import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()

    def registrar(self, data):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(data.password.encode('utf-8'), salt)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # guardo apellido vacio porque la tabla lo pide en la db
            cursor.execute(
                "INSERT INTO user (nombre, numeroCRTl, contraseña, grado, grupo) VALUES (%s, %s, %s, %s, %s)",
                (data.nombre, "", data.numeroCRTL, hashed.decode('utf-8'), data.grado, data.grupo)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()

    def validar_login(self, nombre, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE nombre = %s", (nombre,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['contraseña'].encode('utf-8')):
            return user
        return None
