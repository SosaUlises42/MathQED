import flet as ft
import secrets
import smtplib
import mysql.connector
from email.mime.text import MIMEText

def RecoverView(page: ft.Page, auth_ctrl):

    codigo_generado = ""

    correo_input = ft.TextField(
        label="Correo electrónico",
        width=300,
        border_radius=25,
        border_color="#404040",
        filled=True,
        fill_color="#262626",
        text_style=ft.TextStyle(color="white", size=14),
        label_style=ft.TextStyle(color="#999999", size=13),
        content_padding=20
    )

    codigo_input = ft.TextField(
        label="Código",
        visible=False,
        width=300,
        border_radius=25,
        border_color="#404040",
        filled=True,
        fill_color="#262626",
        text_style=ft.TextStyle(color="white", size=14),
        label_style=ft.TextStyle(color="#999999", size=13),
        content_padding=20
    )

    status_text = ft.Text("")

    verificar_btn = ft.ElevatedButton(
        "Verificar",
        visible=False,
        bgcolor="#2563eb",
        color="white"
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
            page.session.store.set("reset_email", correo_input.value)
            page.go("/confirmacion")

        else:

            status_text.value = (
                "Código incorrecto."
            )

            status_text.color = ft.Colors.RED

        page.update()

    verificar_btn.on_click = verificar_codigo

    return ft.View(

        route="/recover",
        bgcolor="#0d0d0d",
        appbar=ft.AppBar(
            title=ft.Text("MathQED - Recuperacion de Contraseña", color="white"),
            bgcolor="#1a1a1a",
            color="white"
        ),

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
                            weight=ft.FontWeight.BOLD,
                            color="white"
                        ),

                        ft.Text(
                            "Ingresa tu correo para "
                            "recibir un código.",
                            size=14,
                            color="#aaaaaa"
                        ),

                        correo_input,

                        codigo_input,

                        status_text,

                        ft.ElevatedButton(
                            "Enviar código",
                            on_click=enviar_codigo,
                            bgcolor="#2563eb",
                            color="white"
                        ),

                        verificar_btn,

                        ft.TextButton(
                            "Volver al menú",
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.TRANSPARENT,
                                color="#aaaaaa"
                            )
                        )
                    ]
                )
            )
        ]
    )

def Cambiacontraview(page: ft.Page, auth_ctrl):

    correo = page.session.store.get("reset_email") or ""

    pass_input = ft.TextField(
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

    conf_input = ft.TextField(
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

    status_text = ft.Text("")

    volver_login_button = ft.ElevatedButton(
        "Volver a iniciar sesión",
        on_click=lambda e: page.go("/"),
        width=350,
        bgcolor="#2563eb",
        color="white",
        visible=False
    )

    def actualizar_contrasena(nueva_password, usuario_correo):
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mathQED"
        )
        cursor = conexion.cursor()
        try:
            consultas = [
                (
                    "UPDATE user SET Contraseña = %s WHERE Nombre = %s",
                    (nueva_password, usuario_correo)
                ),
                (
                    "UPDATE user SET Contraseña = %s WHERE correo = %s",
                    (nueva_password, usuario_correo)
                ),
                (
                    "UPDATE usuarios SET password = %s WHERE correo = %s",
                    (nueva_password, usuario_correo)
                )
            ]
            for consulta, valores in consultas:
                try:
                    cursor.execute(consulta, valores)
                    if cursor.rowcount > 0:
                        conexion.commit()
                        return True
                except mysql.connector.Error:
                    continue
            conexion.commit()
            return False
        finally:
            cursor.close()
            conexion.close()

    def login_click(e):
        if not pass_input.value or not conf_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, llene todos los campos"))
            page.snack_bar.open = True
            page.update()
            return

        if pass_input.value != conf_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            if not correo:
                raise Exception("No se encontró el correo para resetear contraseña")

            actualizado = actualizar_contrasena(conf_input.value, correo)
            if not actualizado:
                raise Exception("No se encontró el usuario o correo para actualizar")

            status_text.value = "Contraseña actualizada correctamente. Ahora vuelve a iniciar sesión."
            status_text.color = ft.Colors.GREEN
            pass_input.disabled = True
            conf_input.disabled = True
            login_button.visible = False
            volver_login_button.visible = True
            page.update()
        except Exception as ex:
            status_text.value = f"Error al cambiar contraseña: {ex}"
            status_text.color = ft.Colors.RED
            page.update()

    login_button = ft.ElevatedButton(
        "Cambiar contraseña",
        on_click=login_click,
        width=350,
        bgcolor="#2563eb",
        color="white"
    )

    return ft.View(
        route=page.route or "/confirmacion",
        bgcolor="#0d0d0d",
        appbar=ft.AppBar(
            title=ft.Text("MathQED - Recuperacion de Contraseña", color="white"),
            bgcolor="#1a1a1a",
            color="white"
        ),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                [
                    ft.Text("Nueva contraseña", size=24, weight="bold", color="white"),
                    pass_input,
                    conf_input,
                    login_button,
                    volver_login_button,
                    status_text
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                spacing=20
            )
        ]
    )