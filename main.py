import os

import flet as ft  # type:ignore[import-untyped]

from env.classes.paths import paths
from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.config import config
from env.func.logout import logout_on_lost_focus
from env.func.update_themes import update_theme
from env.pages.contacts import ContactsPage
from env.pages.login import LoginPage
from env.pages.settings import SettingsPage


def main(page: ft.Page) -> None:
    # Create app path if it doesn't already exist yet
    os.makedirs(name=paths.app_storage_path, exist_ok=True)

    print(paths.app_storage_path)

    # Initialize window
    page.title = config.APP_TITLE
    page.window.resizable = config.APP_RESIZABLE
    page.window.width = config.APP_WIDTH
    page.window.height = config.APP_HEIGHT

    # Initialize router
    router: AppRouter = AppRouter(page=page)

    # Initialize storage
    storages: Storages = Storages(page=page)

    # TODO: This is only for debugging. Remove this line!
    # storages.client_storage.clear()

    # Update page to apply visuals
    page.update()  # type:ignore

    # Login page
    login_page: LoginPage = LoginPage(page=page, storages=storages, router=router)
    router.add_route(
        route=config.ROUTE_LOGIN,
        content={
            "title": "Login",
            "page_content": [
                login_page.build(),
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
            "execute_function": contacts_page.initialize,
            "function_args": None,
        },
    )

    # Settings page
    settings_page: SettingsPage = SettingsPage(
        page=page,
        router=router,
        storages=storages,
    )
    router.add_route(
        route=config.ROUTE_SETTINGS,
        content={
            "title": "Settings",
            "page_content": [
                settings_page.build(),
            ],
            "execute_function": None,
            "function_args": None,
        },
    )

    # Go to login page
    router.go(route=config.ROUTE_LOGIN)

    # Add events
    # TODO: Add the ability to logout on shaking --> https://flet.dev/docs/controls/shakedetector
    page.on_platform_brightness_change = lambda _: update_theme(page=page)
    page.on_app_lifecycle_state_change = lambda e: logout_on_lost_focus(
        e=e, router=router, storages=storages
    )

    # Update theme
    update_theme(page=page)


if __name__ == "__main__":
    ft.app(target=main)  # type:ignore
