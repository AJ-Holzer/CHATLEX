import flet as ft  # type: ignore[import-untyped]

from env.app.widgets.container import MasterContainer
from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.classes.translations import Translator
from env.config import config
from env.func.calibrations import calibrate_argon2_time_cost


class CalibrationsPage:
    def __init__(
        self,
        page: ft.Page,
        router: AppRouter,
        storages: Storages,
        translator: Translator,
    ) -> None:
        self._page: ft.Page = page
        self._router: AppRouter = router
        self._storages: Storages = storages
        self._translator: Translator = translator

        # Setup calibration UI elements
        self._info_text: ft.Control = self._translator.wrap_control(
            route=config.ROUTE_CALIBRATIONS,
            control_name="info-text",
            control=ft.Text(
                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                text_align=ft.TextAlign.CENTER,
            ),
        )
        self._loading_indicator: ft.ProgressRing = ft.ProgressRing(
            width=80,
            height=80,
            stroke_width=6,
            color=ft.Colors.PRIMARY,
        )
        self._calibration_notice: ft.Control = self._translator.wrap_control(
            route=config.ROUTE_CALIBRATIONS,
            control_name="calibration-notice",
            control=ft.Text(
                theme_style=ft.TextThemeStyle.BODY_LARGE,
                text_align=ft.TextAlign.CENTER,
                opacity=0.7,
            ),
        )

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
        self._translator.update_control_state(
            route=config.ROUTE_CALIBRATIONS,
            control_name="info-text",
            states={
                "value": "calibrate-password-hashing-time-cost",
                "label": None,
                "text": None,
                "helper_text": None,
                "error_text": None,
                "tooltip": None,
            },
        )
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
