from models.usermodel import UsuarioModel
from models.schemasmodel import UsuarioSchema
from pydantic import ValidationError

class AuthController:
    def __init__(self):
        self.model = UsuarioModel()
        
    def login(self, email, password):
        user = self.model.validar_login(email, password)
        if user:
            return user, "Login exitoso"
        return None, "Email o contraseña incorrectos"
        
    def registrar_usuario(self, nombre, email, password):
        try:
            nuevo_usuario = UsuarioSchema(nombre=nombre, email=email, password=password)
            success = self.model.registrar(nuevo_usuario)
            return success ,"Usuario registrado exitosamente." 
        except ValidationError as e:
            return False, e.errors()[0]['msg']