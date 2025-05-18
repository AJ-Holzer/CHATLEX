import flet as ft  # type:ignore[import-untyped]

# Classes
from env.classes.ui import UI
from env.classes.forms import Login

# Themes
from env.themes.themes import themes

def main(page: ft.Page) -> None:
    page.title = "ChatLex"
    page.window.resizable = True
    page.window.width = 400
    page.window.height = 800
    page.fonts = {
        "Varela Round": "fonts/Varela Round.ttf",
        "Baloo Bhaijaan": "fonts/Baloo Bhaijaan.ttf"
    }

    def handle_livecycle_change(e: ft.AppLifecycleStateChangeEvent):
        if e.state not in [ft.AppLifecycleState.SHOW]:
            page.clean()
            page.session.clear()
            page.add(Login(page=page, contrls=[container]))
    
    def update_theme() -> None:
        if page.platform_brightness == ft.Brightness.DARK:
            page.theme = themes.DARK
        else:
            page.theme = themes.LIGHT
        page.update()  # type:ignore

    page.on_platform_brightness_change = lambda _: update_theme()
    page.on_app_lifecycle_state_change = handle_livecycle_change

    update_theme()

    ui: UI = UI(page=page)
    
    # page.client_storage.clear()
    # page.theme_mode = ft.ThemeMode.LIGHT
    
    page.update()  # type:ignore

    container: ft.Container = ft.Container(
        content=ui,
        padding=ft.padding.only(top=40),
        expand=True,
    )

    page.add(Login(page=page, contrls=[container]))
    
    page.on_login
    

if __name__ == "__main__":
    ft.app(target=main, name="ChatLex")  # type:ignore
