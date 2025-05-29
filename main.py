import flet as ft  # type:ignore[import-untyped]

from env.classes.app_storage import Storages
from env.classes.router import AppRouter
from env.config import config
from env.pages.contacts import ContactsPage
from env.pages.login import LoginPage
from env.themes.themes import themes


def update_theme(page: ft.Page) -> None:
    if page.platform_brightness == ft.Brightness.DARK:
        page.theme = themes.DARK
    else:
        page.theme = themes.LIGHT

    page.update()  # type:ignore


def logout_on_lost_focus(
    e: ft.AppLifecycleStateChangeEvent, page: ft.Page, storages: Storages
) -> None:
    if e.state != ft.AppLifecycleState.SHOW:
        # Clear session data and redirect to login
        storages.session_storage.clear()


def main(page: ft.Page) -> None:
    # Initialize window
    page.title = config.APP_TITLE
    page.window.resizable = config.APP_RESIZABLE
    page.window.width = config.APP_WIDTH
    page.window.height = config.APP_HEIGHT
    page.on_platform_brightness_change = lambda _: update_theme(page=page)
    update_theme(page=page)

    # Initialize router
    router: AppRouter = AppRouter(page=page)

    # Initialize storage
    storages: Storages = Storages(page=page)

    # TODO: This is only for debugging. Remove this line!
    storages.client_storage.clear()

    # Update page to apply visuals
    page.update()  # type:ignore

    # Login page
    router.add_route(
        route=config.ROUTE_LOGIN,
        content={
            "title": "Login",
            "page_content": [
                LoginPage(page=page, storages=storages, router=router).build(),
            ],
            "execute_function": None,
            "function_args": None,
        },
    )

    # Contacts Page
    contacts_page: ContactsPage = ContactsPage(
        page=page,
        storages=storages,
        router=router,
    )
    router.add_route(
        route=config.ROUTE_CONTACTS,
        content={
            "title": "Contacts",
            "page_content": [
                contacts_page.build(),
            ],
            "execute_function": contacts_page.load_contacts,
            "function_args": None,
        },
    )

    # Go to login page
    router.go(route=config.ROUTE_LOGIN)


if __name__ == "__main__":
    ft.app(target=main)  # type:ignore
