import flet as ft  # type: ignore[import-untyped]

from env.app.widgets.container import MasterContainer
from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.classes.translate import Translator
from env.config import config
from env.func.calibrations import calibrate_argon2_time_cost


class CalibrationsPage:
    def __init__(
        self,
        page: ft.Page,
        translator: Translator,
        router: AppRouter,
        storages: Storages,
    ) -> None:
        self._page: ft.Page = page
        self._translator: Translator = translator
        self._router: AppRouter = router
        self._storages: Storages = storages

        # Setup calibration UI elements
        self._info_text: ft.Text = ft.Text(
            value="Waiting...",
            theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            text_align=ft.TextAlign.CENTER,
        )
        self._loading_indicator: ft.ProgressRing = ft.ProgressRing(
            width=80,
            height=80,
            stroke_width=6,
            color=ft.Colors.PRIMARY,
        )
        self._calibration_notice: ft.Text = ft.Text(
            value="Lean back while we calibrate your experience.",
            theme_style=ft.TextThemeStyle.BODY_LARGE,
            text_align=ft.TextAlign.CENTER,
            opacity=0.7,
        )

    def _update_info(self, info: str) -> None:
        self._info_text.value = info
        self._info_text.update()

    def calibrate(self) -> None:
        # Skip calibration if already done
        if (
            self._storages.client_storage.get(
                key=config.CS_PASSWORD_HASH_TIME_COST, default=None
            )
            is not None
        ):
            print("Calibrations already completed.")
            self._router.go(config.ROUTE_LOGIN)
            return

        # Perform Argon2 calibration
        self._update_info("Calibrating password hashing time cost...")
        argon2_time_cost: int = calibrate_argon2_time_cost()

        # Save calibration result
        self._storages.client_storage.set(
            key=config.CS_PASSWORD_HASH_TIME_COST,
            value=argon2_time_cost,
        )

        # Redirect to login
        self._router.go(route=config.ROUTE_LOGIN)

    def build(self) -> ft.Container:
        return MasterContainer(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self._info_text,
                            ft.Container(
                                content=self._loading_indicator,
                                margin=ft.margin.only(top=20, bottom=20),
                            ),
                            self._calibration_notice,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        )
