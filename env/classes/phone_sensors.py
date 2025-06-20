import flet as ft  # type:ignore[import-untyped]

from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.config import config
from env.func.logout import logout


class ShakeDetector:
    def __init__(self, page: ft.Page, router: AppRouter, storages: Storages) -> None:
        self._page: ft.Page = page
        self._router: AppRouter = router
        self._storages: Storages = storages

        # Initialize shake detector instance
        self._shake_detector: ft.ShakeDetector = ft.ShakeDetector(
            shake_threshold_gravity=config.SHAKE_THRESHOLD_GRAVITY,
            on_shake=lambda _: logout(router=self._router, storages=self._storages),
        )

    def enable(self) -> None:
        self._page.overlay.append(self._shake_detector)

    def disable(self) -> None:
        if self._shake_detector not in self._page.overlay:
            return

        self._page.overlay.remove(self._shake_detector)

    @property
    def shake_detector(self) -> ft.ShakeDetector:
        return self._shake_detector
