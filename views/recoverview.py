import flet as ft
import secrets
import smtplib
import mysql.connector

from email.mime.text import MIMEText


def RecoverView(page: ft.Page, auth_ctrl):

    codigo_generado = ""

    correo_input = ft.TextField(
        label="Correo electrónico",
        width=300
    )

    codigo_input = ft.TextField(
        label="Código",
        visible=False,
        width=300
    )

    status_text = ft.Text("")

    verificar_btn = ft.ElevatedButton(
        "Verificar",
        visible=False
    )

    # FUNCIÓN PARA ENVIAR CORREO
    def enviar_correo(destinatario, codigo):

        correo = "matqedorg@gmail.com"

        password = "zkla kvyd qaaj bbee"

        mensaje = MIMEText(
            f"""
Hola.

Tu código de recuperación de MathQED es:

{codigo}

Si no solicitaste este código, ignora este mensaje.
"""
        )

        mensaje["Subject"] = (
            "MathQED - Recuperación"
        )

        mensaje["From"] = correo

        mensaje["To"] = destinatario

        servidor = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        servidor.starttls()

        servidor.login(
            correo,
            password
        )

        servidor.send_message(mensaje)

        servidor.quit()

    # ENVIAR CÓDIGO
    def enviar_codigo(e):

        nonlocal codigo_generado

        if not correo_input.value:

            status_text.value = (
                "Ingresa un correo."
            )

            status_text.color = ft.Colors.RED

            page.update()

            return

        codigo_generado = str(
            secrets.randbelow(900000) + 100000
        )

        try:

            enviar_correo(
                correo_input.value,
                codigo_generado
            )

            codigo_input.visible = True

            verificar_btn.visible = True

            status_text.value = (
                "Código enviado correctamente."
            )

            status_text.color = ft.Colors.GREEN

        except Exception as ex:

            status_text.value = (
                f"Error: {ex}"
            )

            status_text.color = ft.Colors.RED

        page.update()

    # VERIFICAR
    def verificar_codigo(e):

        if codigo_input.value == codigo_generado:

            status_text.value = (
                "Código correcto."
            )

            status_text.color = ft.Colors.GREEN
            page.go(f"/confirmacion/{correo_input.value}")

        else:

            status_text.value = (
                "Código incorrecto."
            )

            status_text.color = ft.Colors.RED

        page.update()

    verificar_btn.on_click = verificar_codigo

    return ft.View(

        route="/recover",

        controls=[

            ft.Container(

                expand=True,

                alignment=ft.Alignment(0, 0),

                content=ft.Column(

                    horizontal_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),

                    alignment=(
                        ft.MainAxisAlignment.CENTER
                    ),

                    controls=[

                        ft.Text(
                            "Recuperar contraseña",
                            size=25,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            "Ingresa tu correo para "
                            "recibir un código.",
                            size=14
                        ),

                        correo_input,

                        codigo_input,

                        status_text,

                        ft.ElevatedButton(
                            "Enviar código",
                            on_click=enviar_codigo
                        ),

                        verificar_btn
                    ]
                )
            )
        ]
    )

def Cambiacontraview(page: ft.Page, auth_ctrl, correo):

    pass_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=10
    )

    conf_input = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=10
    )

    def login_click(e):
        if not pass_input.value or not conf_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, llene todos los campos"))
            page.snack_bar.open = True
            page.update()
        elif pass_input.value != conf_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coninciden"))
            page.snack_bar.open = True
            page.update()
        else:
            conexion = mysql.connector.connect(

                host="localhost",
                user="root",
                password="",
                database="mathQED"

            )

            cursor = conexion.cursor()

            consulta = """
            UPDATE usuarios
            SET password = %s
            WHERE correo = %s
            """

            valores = (
                conf_input.value,
                correo
            )

            cursor.execute(
                consulta,
                valores
            )

            conexion.commit()

            cursor.close()

            conexion.close()

            print("Contraseña actualizada")
            page.go("/dashboard")  


    login_button = ft.ElevatedButton(
        "Entrar",
        on_click=login_click,
        width=350,
        bgcolor="blue",
        color="white"
    )

    return ft.View(
        route="/confirmacion",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                [
                    ft.Text("Nueva contraseña", size=24, weight="bold"),
                    conf_input,
                    pass_input,
                    login_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                spacing=20
            )
        ]
    )