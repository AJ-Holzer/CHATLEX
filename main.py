import flet as ft  # type:ignore[import-untyped]

# Classes
from env.classes.ui import UI
from env.classes.forms import Login

# Func
from env.func.get_session_key import get_key_or_default

# Themes
from env.themes.themes import themes

# Config
from env.config import config

def main(page: ft.Page) -> None:
    page.title = "ChatLex"
    page.window.resizable = True
    page.window.width = 400
    page.window.height = 800
    page.fonts = {
        "Varela Round": "fonts/Varela Round.ttf",
        "Baloo Bhaijaan": "fonts/Baloo Bhaijaan.ttf"
    }
    
    logout_on_lost_focus: bool = get_key_or_default(page=page, default=config.LOGOUT_ON_LOST_FOCUS_DEFAULT, key_name=config.CS_LOGOUT_ON_LOST_FOCUS)

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
    if logout_on_lost_focus:
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
