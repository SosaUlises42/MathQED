import flet as ft 
from controllers.usercontroller import AuthController
from views.loginview import LoginView
from views.dashboardview import RegisterView

def start(page: ft.Page):
    # Configuración básica de la página
    page.title = "SIGE - Sistema de Gestión"
    page.window_width = 450
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    
    print("Iniciando aplicación...")

    # Cargamos los controladores
    try:
        auth_ctrl = AuthController()
        print("Controladores cargados exitosamente.")
    except Exception as ex:
        print(f"Error al iniciar controladores: {ex}")

    def route_change(e):
        print(f"Cambiando ruta a: {page.route}")
        page.views.clear()
        # rutas de la app: login, registro y dashboard
        if page.route == "/" or page.route == "":
            print("Cargando LoginView...")
            page.views.append(LoginView(page, auth_ctrl))
            
        elif page.route == "/registro":
            print("Cargando RegisterView...")
            page.views.append(RegisterView(page, auth_ctrl))
            
            
        
        # seguridad por si la ruta no existe
        if not page.views:
            page.views.append(
                ft.View("/", [ft.Text("Error 404: Ruta no encontrada")])
            )

        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    # Configuramos los eventos de la página
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # AJUSTE FINAL: En lugar de page.go, llamamos directamente a la función
    # para asegurar que la primera vista se cargue sin errores de tiempo.
    route_change(None) 
    page.update()

def main():
    print("Arrancando Flet Engine...")
    ft.app(target=start)

if __name__ == "__main__":
    main()