import flet as ft 
from src.controllers.usercontroller import AuthController
from src.controllers.promptcontroller import Request
from src.views.loginview import LoginView
from src.views.dashboardview import RegisterView, DashboardView, toPromptController
from src.views.recoverview import RecoverView, Cambiacontraview
from src.views.chatview import chatView

def start(page: ft.Page):
    # Configuración básica de la página
    page.title = "MathQED - Chatbot de Matematicas"
    page.window_width = 450
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    
    print("Iniciando aplicación...")

    # Cargamos los controladores
    try:
        auth_ctrl = AuthController()
        prmt_crtl = Request()
        print("Controladores cargados exitosamente.")
    except Exception as ex:
        print(f"Error al iniciar controladores: {ex}")

    def route_change(e):
        route = page.route or "/"
        print(f"Cambiando ruta a: {route}")
        page.views.clear()
        # rutas de la app: login, registro y dashboard
        if route == "/":
            print("Cargando LoginView...")
            page.views.append(LoginView(page, auth_ctrl))
        elif route == "/registro":
            print("Cargando RegisterView...")
            page.views.append(RegisterView(page, auth_ctrl))
        elif route == "/dashboard":
            print("Cargando DashboardView...")
            page.views.append(DashboardView(page, prmt_crtl))
        elif route == "/refresh":
            page.views.append(toPromptController(page, prmt_crtl))
        elif route == "/recover":
            page.views.append(RecoverView(page, auth_ctrl))
        elif route == "/confirmacion":
            page.views.append(Cambiacontraview(page, auth_ctrl))
        elif route == "/chat":
            page.views.append(chatView(page, prmt_crtl))

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

    # Forzamos inicio en ruta principal para no usar rutas anteriores del historial.
    page.views.append(LoginView(page, auth_ctrl))
    page.update()
    page.go("/")

def main():
    print("Arrancando Flet Engine...")
    ft.app(target=start)

if __name__ == "__main__":
    main()