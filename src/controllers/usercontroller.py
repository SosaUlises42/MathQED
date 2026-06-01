from src.models.usermodel import UsuarioModel
from src.models.schemasmodel import UsuarioSchema
from pydantic import ValidationError

class AuthController:
    def __init__(self):
        self.model = UsuarioModel()
        
    def login(self, nombre, password):
        user = self.model.validar_login(nombre, password)
        if user:
            return user, "Login exitoso"
        return None, "Email o contraseña incorrectos"
        
    def registrar_usuario(self, nombre, email, crtl, password, grado, grupo):

        print(nombre)
        print(crtl)
        print(email)
        print(password)
        print(grado)
        print(grupo)

        try:
            nuevo_usuario = UsuarioSchema(nombre=nombre, email=email, control=crtl, password=password, grado=grado, grupo=grupo)
            success = self.model.registrar(nuevo_usuario)
            return success ,"Usuario registrado exitosamente." 
        except ValidationError as e:
            print(e)
            return False, e.errors()[0]['msg']