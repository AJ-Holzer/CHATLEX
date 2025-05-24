import flet as ft  # type:ignore[import-untyped]

from env.classes.forms import Login
from env.classes.pages import Router
from env.classes.routes import ContactsPage
from env.config import config
from env.func.get_session_key import get_key_or_default
from env.themes.themes import themes

# from env.classes.database import DatabaseHandler
# from env.classes.ui import UI


def main(page: ft.Page) -> None:
    """Initializes and configures the main application page.

    Args:
        page(ft.Page): The FlutterFlow page object.

    Returns:
        None: No return value.

    Raises:
        Exception: Generic exception during page initialization or configuration.
    """
    page.title = "ChatLex"
    page.window.resizable = True
    page.window.width = 400
    page.window.height = 800
    page.fonts = {
        "Varela Round": "fonts/Varela Round.ttf",
        "Baloo Bhaijaan": "fonts/Baloo Bhaijaan.ttf",
    }

    def handle_livecycle_change(e: ft.AppLifecycleStateChangeEvent):
        if e.state not in [ft.AppLifecycleState.SHOW]:
            # Clear session data and redirect to login
            page.session.clear()
            page.go(config.ROUTE_LOGIN)

    def update_theme() -> None:
        if page.platform_brightness == ft.Brightness.DARK:
            page.theme = themes.DARK
        else:
            page.theme = themes.LIGHT
        page.update()  # type:ignore

    logout_on_lost_focus: bool = get_key_or_default(
        page=page,
        default=config.LOGOUT_ON_LOST_FOCUS_DEFAULT,
        key_name=config.CS_LOGOUT_ON_LOST_FOCUS,
    )

    router: Router = Router(
        page=page,
        start_route=config.ROUTE_LOGIN,
    )

    # Login page
    router.add(
        route=config.ROUTE_LOGIN,
        content={
            "title": "Login",
            "content": [
                Login(page=page, router=router),
            ],
        },
    )

    # Contacts page
    router.add(
        route=config.ROUTE_CONTACTS,
        content={
            "title": "Contacts",
            "content": [ContactsPage(page=page, router=router).build()],
        },
    )

    # TODO: Create contacts page
    # TODO: Create chat page for each contact
    # TODO: Create settings page
    # TODO: Create about page
    # TODO: Create user profile page

    # page.theme_mode = ft.ThemeMode.LIGHT

    # ui_container: ft.Container = ft.Container(
    #     content=ui,
    #     padding=ft.padding.only(top=40),
    #     expand=True,
    # )

    # page.add(Login(page=page, contrls=[container]))

    page.on_platform_brightness_change = lambda _: update_theme()
    if logout_on_lost_focus:
        page.on_app_lifecycle_state_change = handle_livecycle_change

    update_theme()

    router.go(config.ROUTE_LOGIN)


if __name__ == "__main__":
    ft.app(target=main, name="ChatLex")  # type:ignore
