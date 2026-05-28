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

        print(data)

        try:
            # guardo valores vacíos para los campos requeridos por la tabla
            cursor.execute(
                "INSERT INTO user (nombre, correo, numeroCRTl, Password_Hash, grado, grupo) VALUES (%s, %s, %s, %s, %s, %s)",
                (data.nombre, data.email ,data.control , hashed.decode('utf-8'), data.grado, data.grupo)
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
        cursor.execute(
            "SELECT Usuario_ID, Nombre, correo, NumeroCRTL, Password_Hash AS Password_Hash, Grado, Grupo FROM user WHERE Nombre = %s",
            (nombre,)
        )
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['Password_Hash'].encode('utf-8')):
            return user
        return None
