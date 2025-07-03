import flet as ft  # type: ignore[import-untyped]

from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.config import config
from env.func.logout import logout


class ShakeDetector:
    def __init__(self, page: ft.Page, router: AppRouter, storages: Storages) -> None:
        self._page: ft.Page = page
        self._router: AppRouter = router
        self._storages: Storages = storages

        # Whether the shake detector is enabled
        self._enabled: bool = True

        # Initialize shake detector instance
        self._shake_detector: ft.ShakeDetector = ft.ShakeDetector(
            shake_threshold_gravity=config.SHAKE_DETECTION_THRESHOLD_GRAVITY_DEFAULT,
            on_shake=self._logout,
        )

        # Add event to page overlay
        self._page.overlay.append(self._shake_detector)
        self._page.update()  # type: ignore

    def _logout(self, e: ft.ControlEvent) -> None:
        # Skip if disabled
        if not self._enabled:
            return

        # Skip if setting is set to 'False'
        if not self._storages.client_storage.get(
            key=config.CS_SHAKE_DETECTION_ENABLED,
            default=config.SHAKE_DETECTION_ENABLED_DEFAULT,
        ):
            return

        logout(router=self._router, storages=self._storages)

    @property
    def gravity_threshold(self) -> float:
        return self.gravity_threshold

    @gravity_threshold.setter
    def gravity_threshold(self, value: float) -> None:
        self._shake_detector.shake_threshold_gravity = value

        self._page.update()  # type: ignore

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
