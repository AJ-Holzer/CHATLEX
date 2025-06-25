import flet as ft  # type:ignore[import-untyped]

from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.func.logout import logout_on_lost_focus


class FocusDetector:
    def __init__(self, page: ft.Page, router: AppRouter, storages: Storages) -> None:
        self._page: ft.Page = page
        self._router: AppRouter = router
        self._storages: Storages = storages

        # Enable focus detection
        self._enabled: bool = True

        # Add event to page
        page.on_app_lifecycle_state_change = self._logout

    def _logout(self, e: ft.AppLifecycleStateChangeEvent) -> None:
        # Check if enabled
        if not self._enabled:
            return

        # Logout
        logout_on_lost_focus(
            e=e,
            router=self._router,
            storages=self._storages,
        )

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
