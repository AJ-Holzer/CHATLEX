import os

import flet as ft  # type:ignore[import-untyped]

from env.classes.paths import paths
from env.classes.phone_sensors import ShakeDetector
from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.config import config
from env.func.logout import logout_on_lost_focus
from env.pages.calibration import CalibrationsPage
from env.pages.contacts import ContactsPage
from env.pages.login import LoginPage
from env.pages.profiles import UserProfilePage
from env.pages.settings import SettingsPage
from env.themes.themes import Themes


def main(page: ft.Page) -> None:
    # Create app path if it doesn't already exist yet
    os.makedirs(name=paths.app_storage_path, exist_ok=True)

    print(paths.app_storage_path)

    # Initialize window
    page.title = config.APP_TITLE
    page.window.resizable = config.APP_RESIZABLE
    page.window.width = config.APP_WIDTH
    page.window.height = config.APP_HEIGHT

    # TODO: Add the ability to add more fonts (online)
    # Add global fonts
    page.fonts = config.FONT_FAMILIES_LOCAL

    # Initialize router
    router: AppRouter = AppRouter(page=page)

    # Initialize storage
    storages: Storages = Storages(page=page)

    # Initialize shake detector for logging out on shaking
    shake_detector: ShakeDetector = ShakeDetector(
        page=page,
        router=router,
        storages=storages,
    )

    # Initialize themes
    themes: Themes = Themes(page=page, storages=storages)

    # Apply theme
    themes.set_theme()

    # Update page to apply visuals
    page.update()  # type:ignore

    # Login page
    login_page: LoginPage = LoginPage(
        page=page,
        storages=storages,
        router=router,
        shake_detector=shake_detector,
    )
    router.add_route(
        route=config.ROUTE_LOGIN,
        content={
            "title": "Login",
            "page_content": [
                login_page.build(),
            ],
            "execute_function": login_page.initialize,
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
        themes=themes,
        shake_detector=shake_detector,
    )
    router.add_route(
        route=config.ROUTE_SETTINGS,
        content={
            "title": "Settings",
            "page_content": [
                settings_page.build(),
            ],
            "execute_function": settings_page.initialize,
            "function_args": None,
        },
    )

    # User profile page
    user_profile_page: UserProfilePage = UserProfilePage(
        page=page,
        router=router,
        storages=storages,
    )
    router.add_route(
        route="/profile",
        content={
            "title": "Profile",
            "page_content": [
                user_profile_page.build(),
            ],
            "execute_function": None,
            "function_args": None,
        },
    )

    # Calibration page
    calibration_page: CalibrationsPage = CalibrationsPage(
        page=page,
        router=router,
        storages=storages,
    )
    router.add_route(
        route=config.ROUTE_CALIBRATIONS,
        content={
            "title": "Calibration",
            "page_content": [calibration_page.build()],
            "execute_function": calibration_page.calibrate,
            "function_args": None,
        },
    )

    # Go to login page
    router.go(route=config.ROUTE_CALIBRATIONS)

    # Add events
    page.on_platform_brightness_change = lambda _: themes.set_theme()
    page.on_app_lifecycle_state_change = lambda e: logout_on_lost_focus(
        e=e, router=router, storages=storages
    )


if __name__ == "__main__":
    ft.app(target=main)  # type:ignore
