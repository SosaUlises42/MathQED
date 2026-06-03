import flet as ft
from collections import deque
from src.models.databasemodel import Database

def historialView(page: ft.Page, Request):

    tarjetas = []

    for x in Request.histo:

        if x["autor"] == "ejercicio":
            ejercicio = x["mensaje"]

        elif x["autor"] == "result" and ejercicio:

            tarjetas.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                ejercicio,
                                color="white",
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                x["mensaje"],
                                color="#aaaaaa",
                                size=14
                            ),
                        ],
                        spacing=5
                    ),
                bgcolor="#1a1a1a",
                border_radius=15,
                padding=15,
                margin=5
            )
        )

    return ft.View(

        route="/historial",

        bgcolor="#0d0d0d",

        appbar=ft.AppBar(
            title=ft.Text(
                "MathQED - Historial",
                color="white"
            ),

            bgcolor="#1a1a1a",

            actions=[
                ft.TextButton(
                    "Volver",
                    style=ft.ButtonStyle(
                        color="white"
                    ),
                    on_click=lambda e: page.go("/chat")
                )
            ]
        ),

        controls=[

            ft.Container(

                expand=True,

                padding=20,

                content=ft.Column(

                    [
                        ft.Text(
                            "Historial de consultas",
                            color="white",
                            size=24,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Divider(color="#222222"),

                        ft.ListView(
                            controls=tarjetas,
                            expand=True,
                            spacing=10
                        )
                    ],

                    expand=True,
                    scroll=ft.ScrollMode.AUTO
                )
            )
        ]
    )

def setHistorial(page, Request):

    usuario = page.session.store.get("user")
    us_id = usuario["Usuario_ID"]

    conn = Database.get_connection()
    cursor = conn.cursor()

    ejercicio = None

    for x in Request.mensajes:

        if x["autor"] == "ejercicio":
            ejercicio = x["mensaje"]

        elif x["autor"] == "result" and ejercicio:

            cursor.execute(
                """
                INSERT INTO historial
                (Ejercicio, Resultado, Usuario_ID)
                VALUES (%s, %s, %s)
                """,
                (ejercicio, x["mensaje"], us_id)
            )

            ejercicio = None

    conn.commit()

    cursor.close()
    conn.close()
    page.go("/chat")

def getHistorial(page: ft.Page, Request):
    usuario = page.session.store.get("user")
    us_id = usuario["Usuario_ID"]

    wh = page.session.store.get("where")

    conn = Database.get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM historial
        WHERE Usuario_ID = %s
        """,
        (us_id,)
    )

    historial = cursor.fetchall()
    cursor.close()
    conn.close()

    Request.mensajes.clear()
    Request.histo.clear()

    for x in historial:
        Request.histo.append({
            'autor': "ejercicio",
            'mensaje': x["Ejercicio"]
        })
        Request.histo.append({
            'autor': "result",
            'mensaje': x["Resultado"]
        })

    for x in historial:
        Request.mensajes.append({
            'autor': "ejercicio",
            'mensaje': x["Ejercicio"]
        })
        Request.mensajes.append({
            'autor': "result",
            'mensaje': x["Resultado"]
        })

        while len(Request.mensajes) > 10:
            Request.mensajes.pop(0)

    if wh == "login":
        page.go("/dashboard")
    elif wh == "chat":
        page.go("/historial")
