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

        # Whether shake detection is enabled
        self._enabled: bool = self._storages.client_storage.get(
            key=config.CS_SHAKE_DETECTION,
            default=config.SHAKE_ENABLED_DEFAULT,
        )

        # Initialize shake detector instance
        self._shake_detector: ft.ShakeDetector = ft.ShakeDetector(
            shake_threshold_gravity=config.SHAKE_THRESHOLD_GRAVITY,
            on_shake=lambda _: self._logout(),
        )

    def _logout(self) -> None:
        # Skip if setting is set to 'False'
        if (
            not self._storages.client_storage.get(
                key=config.CS_SHAKE_DETECTION, default=config.SHAKE_ENABLED_DEFAULT
            )
            or not self._enabled
        ):
            return

        logout(router=self._router, storages=self._storages)

    def enable(self) -> None:
        if self._shake_detector in self._page.overlay or self._enabled:
            return

        self._page.overlay.append(self._shake_detector)
        self._page.update()  # type:ignore

    def disable(self) -> None:
        if self._shake_detector not in self._page.overlay or not self._enabled:
            return

        self._page.overlay.remove(self._shake_detector)
        self._page.update()  # type:ignore

    @property
    def shake_detector(self) -> ft.ShakeDetector:
        return self._shake_detector
