import flet as ft

def chatView(page: ft.Page, Request):

    chat_globe = []
    for mensaje in Request.mensajes:
        print(len(chat_globe))
        if mensaje["autor"] == 'user':
            chat_globe.append(
                ft.Container(
                    content=ft.Text(
                        mensaje['mensaje'],
                        color="white",
                        size=15
                    ),
                    width=page.window.width * 0.75,
                    bgcolor="#2563eb",
                    padding=15,
                    border_radius=20,
                    margin=5,
                    alignment=ft.Alignment(1, 0)
                )
            )
        else:
            chat_globe.append(
                ft.Container(
                    content=ft.Text(
                        mensaje['mensaje'],
                        color="white",
                        size=15
                    ),
                    width=page.window.width * 0.75,
                    bgcolor="#1f1f1f",
                    padding=15,
                    border_radius=20,
                    margin=5,
                    alignment=ft.Alignment(-1, 0)
                )
            )

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
        max_lines=1,
        multiline=False,
        on_submit=lambda e: click(e)
    )

    def click(e):
        if not request_input.value or not request_input.value.strip():
            Request.stringChat("machine", "Por favor escribe algo antes de enviar.")
            page.go("/chat")
            return
        page.session.store.set("last_msg", request_input.value)
        page.go("/refresh")

    send_button = ft.IconButton(
        icon=ft.Icons.ARROW_FORWARD,
        icon_color="white",
        bgcolor="#2563eb",
        icon_size=22,                           
        on_click=lambda e: click(e)
    )

    request_row = ft.Row(
        [request_input, send_button],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.END,
        spacing=10
    )

    return ft.View(
        route="/chat",
        bgcolor="#0d0d0d",

        appbar=ft.AppBar(
            title=ft.Text(
                "MathQED - Nuevo Chat",
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
                content=ft.Column(

                    [
                        ft.Column(
                            controls=chat_globe,
                            expand=True,
                            scroll=ft.ScrollMode.AUTO
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
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        ]
    )