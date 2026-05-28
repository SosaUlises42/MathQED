import flet as ft

def RegisterView(page: ft.Page, auth_controller):
    # registro en el mismo archivo dashboardView para no usar registerView.py
    nombre_input = ft.TextField(
        label="Nombre completo",
        input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]*",
            replacement_string=""
        ),
        width=350,
        border_radius=25,
        border_color="#404040",
        filled=True,
        fill_color="#262626",
        text_style=ft.TextStyle(color="white", size=14),
        label_style=ft.TextStyle(color="#999999", size=13),
        content_padding=20
    )

    email_input = ft.TextField(
        label="Correo electrónico",
        width=350,
        border_radius=25,
        border_color="#404040",
        filled=True,
        fill_color="#262626",
        text_style=ft.TextStyle(color="white", size=14),
        label_style=ft.TextStyle(color="#999999", size=13),
        content_padding=20,
        keyboard_type=ft.KeyboardType.EMAIL
    )

    crtl_input = ft.TextField(
        label="Numero de Control",
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        max_length=14,
        width=350,
        border_radius=25,
        border_color="#404040",
        filled=True,
        fill_color="#262626",
        text_style=ft.TextStyle(color="white", size=14),
        label_style=ft.TextStyle(color="#999999", size=13),
        content_padding=20
    )

    password_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=25,
        border_color="#404040",
        filled=True,
        fill_color="#262626",
        text_style=ft.TextStyle(color="white", size=14),
        label_style=ft.TextStyle(color="#999999", size=13),
        content_padding=20
    )

    password_confirm_input = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=25,
        border_color="#404040",
        filled=True,
        fill_color="#262626",
        text_style=ft.TextStyle(color="white", size=14),
        label_style=ft.TextStyle(color="#999999", size=13),
        content_padding=20
    )

    grado_input = ft.TextField(
        label="Grado",
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        max_length=1,
        width=350,
        border_radius=25,
        border_color="#404040",
        filled=True,
        fill_color="#262626",
        text_style=ft.TextStyle(color="white", size=14),
        label_style=ft.TextStyle(color="#999999", size=13),
        content_padding=20
    )

    grupo_input = ft.TextField(
        label="Grupo",
        input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]*",
            replacement_string=""
        ),
        max_length=1,
        width=350,
        border_radius=25,
        border_color="#404040",
        filled=True,
        fill_color="#262626",
        text_style=ft.TextStyle(color="white", size=14),
        label_style=ft.TextStyle(color="#999999", size=13),
        content_padding=20
    )

    def register_click(e):
        if not nombre_input.value or not email_input.value or not password_input.value or not password_confirm_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, llene todos los campos"))
            page.snack_bar.open = True
            page.update()
            return

        if password_input.value != password_confirm_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden"))
            page.snack_bar.open = True
            page.update()
            return

        success, msg = auth_controller.registrar_usuario(
            nombre_input.value,
            email_input.value,
            crtl_input.value,
            password_input.value,
            grado_input.value,
            grupo_input.value
        )

        print(nombre_input.value)
        print(email_input.value)
        print(crtl_input.value)
        print(password_input.value)
        print(grado_input.value)
        print(grupo_input.value)

        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

        if success:
            page.go("/")

    register_button = ft.ElevatedButton(
        "Registrar cuenta",
        on_click=register_click,
        width=350,
        bgcolor="#2563eb",
        color="white"
    )

    return ft.View(
        route="/registro",
        bgcolor="#0d0d0d",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("MathQED - Registro", color="white"),
            bgcolor="#1a1a1a",
            color="white"
        ),
        controls=[
            ft.Column(
                [
                    ft.Text("Crear una cuenta nueva", size=24, weight="bold", color="white"),
                    nombre_input,
                    email_input,
                    crtl_input,
                    password_input,
                    password_confirm_input,
                    grado_input,
                    grupo_input,
                    register_button,
                    ft.TextButton(
                        "Volver al login",
                        on_click=lambda _: page.go("/"),
                        style=ft.ButtonStyle(color="#aaaaaa")
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                spacing=20
            )
        ]
    )


def DashboardView(page: ft.Page, auth_controller):

    usuario = page.session.store.get("user")
    print(usuario)
    nombre = usuario["Nombre"]

    request_input = ft.TextField(
        label="Realiza una solicitud",
        width=400,
        border_radius=25,
        border_color="#404040",
        filled=True,
        fill_color="#262626",
        text_style=ft.TextStyle(color="white", size=14),
        label_style=ft.TextStyle(color="#999999", size=13),
        content_padding=20,
        min_lines=1,
        max_lines=3,
        multiline=True
    )

    def send_request_click(e):
        if request_input.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text(f"Solicitud enviada: {request_input.value}"))
            page.snack_bar.open = True
            request_input.value = ""
            page.update()

    request_row = ft.Row(
        [request_input],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.END,
        spacing=10
    )

    return ft.View(

    route="/dashboard",

    bgcolor="#0d0d0d",

    appbar=ft.AppBar(

        title=ft.Text(
            "MathQED - Dashboard",
            color="white"
        ),

        bgcolor="#1a1a1a",

        actions=[

            ft.TextButton(

                "Salir",

                style=ft.ButtonStyle(
                    color="white"
                ),

                on_click=lambda _:
                page.go("/")
            )
        ]
    ),

    controls=[

        ft.Container(

            expand=True,

            alignment=ft.Alignment(0, 0),

            content=ft.Column(

                [

                    ft.Text(

                        f"Bienvenido de nuevo {nombre}",

                        size=32,

                        weight="bold",

                        color="white"
                    ),

                    ft.Text(

                        "¿Con qué puedo ayudarte hoy?",

                        color="#aaaaaa",

                        size=16
                    ),

                    ft.Row(

                        [

                            ft.Container(

                                content=request_row,

                                border_radius=20,

                                shadow=ft.BoxShadow(

                                    spread_radius=1,

                                    blur_radius=20,

                                    color="#222222"
                                )
                            ),

                            ft.Container(

                                content=ft.IconButton(

                                    icon=ft.Icons.ARROW_FORWARD,

                                    icon_color="white",

                                    bgcolor="#2563eb",

                                    icon_size=22
                                ),

                                border_radius=100,

                                shadow=ft.BoxShadow(

                                    spread_radius=1,

                                    blur_radius=15,

                                    color="#2563eb55"
                                )
                            )
                        ],

                        alignment=ft.MainAxisAlignment.CENTER
                    )

                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                alignment=ft.MainAxisAlignment.CENTER,

                spacing=25
            )
        )
    ]
)