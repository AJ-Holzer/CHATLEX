from typing import Optional

import flet as ft  # type:ignore[import-untyped]

from env.classes.app_storage import Storages
from env.classes.router import AppRouter
from env.config import config


def logout_on_lost_focus(
    e: Optional[ft.AppLifecycleStateChangeEvent],
    router: AppRouter,
    storages: Storages,
    force: bool = False,
) -> None:
    # Skip if setting is not explicitly set to 'True'
    if (
        not storages.client_storage.get(
            key=config.CS_LOGOUT_ON_LOST_FOCUS,
            default=config.LOGOUT_ON_LOST_FOCUS_DEFAULT,
        )
        and not force
    ):
        return

    # Check if focus lost
    if e is None or e.state != ft.AppLifecycleState.SHOW:
        # Clear session data and redirect to login
        storages.session_storage.clear()
        router.go(route=config.ROUTE_LOGIN)
