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
                "INSERT INTO usuario (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)",
                (data.nombre, "", data.email, hashed.decode('utf-8'))
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()

    def validar_login(self, email, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user
        return None

class TareasModel:
    def __init__(self):
        self.db = Database()

    def crear_tarea(self, data, usuario_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tareas (titulo, descripcion, prioridad, clasificacion, usuario_id) VALUES (%s, %s, %s, %s, %s)",
                (data.titulo, data.descripcion, data.prioridad, data.clasificacion, usuario_id)
            )
            conn.commit()
            return True
        finally:
            conn.close()

    def obtener_tareas(self, usuario_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tareas WHERE usuario_id = %s", (usuario_id,))
        tareas = cursor.fetchall()
        conn.close()
        return tareas