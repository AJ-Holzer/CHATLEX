from typing import Optional

import flet as ft  # type:ignore[import-untyped]

from env.app.widgets.container import MasterContainer
from env.classes.app_storage import Storages
from env.classes.encryption import AES
from env.classes.hashing import ArgonHasher
from env.classes.router import AppRouter
from env.config import config
from env.func.converter import byte_to_str, str_to_byte


class LoginPage:
    def __init__(self, page: ft.Page, storages: Storages, router: AppRouter) -> None:
        # Initialize page
        self._page: ft.Page = page
        self._storages: Storages = storages
        self._router: AppRouter = router

        # User stuff
        self._user_already_exists: bool = bool(
            self._storages.client_storage.get(key=config.CS_USER_PASSWORD_HASH)
        ) and bool(self._storages.client_storage.get(key=config.CS_USER_PASSWORD_IV))

        # Password stuff
        self._password_hash: Optional[str] = storages.client_storage.get(
            key=config.CS_USER_PASSWORD_HASH
        )
        self._salt: Optional[bytes] = str_to_byte(
            data=self._storages.client_storage.get(key=config.CS_USER_SALT)
        )

        # Initialize hasher and encryptor
        self._hasher: ArgonHasher = ArgonHasher()

        # Entries
        self._entry_password: ft.TextField = ft.TextField(
            label="Password", password=True, on_change=self._validate
        )
        if not self._user_already_exists:
            self._entry_password_confirmation: ft.TextField = ft.TextField(
                label="Confirm Password", password=True, on_change=self._validate
            )

        # Buttons
        self._button_submit: ft.ElevatedButton = ft.ElevatedButton(
            text="Login" if self._user_already_exists else "Create Account",
            on_click=self._login if self._user_already_exists else self._create_account,
            disabled=True,
        )

        # Progress bar
        self._progress_bar: ft.ProgressBar = ft.ProgressBar(visible=False)

        self.show_info_dialog()  # FIXME: The alert can't be closed somehow!??

    def _progress_visible(self, visible: bool) -> None:
        self._progress_bar.visible = visible
        self._progress_bar.update()

    def _button_clickable(self, clickable: bool) -> None:
        self._button_submit.disabled = not clickable
        self._button_submit.update()

    def _validate(self, e: ft.ControlEvent) -> None:
        self._button_submit.disabled = (
            False
            if all(
                [
                    self._entry_password.value,
                    *(
                        [self._entry_password_confirmation.value]
                        if not self._user_already_exists
                        else []
                    ),
                ]
            )
            else True
        )

        self._button_submit.update()  # type:ignore

    def _create_account(self, e: ft.ControlEvent) -> None:
        # Give the user feedback that something happens
        self._button_clickable(clickable=False)
        self._progress_visible(visible=True)

        if self._entry_password.value != self._entry_password_confirmation.value:
            pwd_not_equal_alert: ft.AlertDialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(value="Incorrect Password!"),
                content=ft.Text(
                    value="The passwords you entered are not equal! Please enter them again."
                ),
                actions=[
                    ft.TextButton(
                        text="OK",
                        on_click=lambda e: self._page.close(pwd_not_equal_alert),
                    )
                ],
            )
            self._page.open(pwd_not_equal_alert)

            # Enable the button again and hide progress bar
            self._button_clickable(clickable=True)
            self._progress_visible(visible=False)
            return

        # Initialize encryptor
        encryptor: AES = AES(password=str(self._entry_password.value))

        # Generate salt and iv
        encryptor.generate_iv()
        encryptor.generate_salt()

        # Show progress bar to indicate something is happening
        self._progress_visible(visible=True)

        iv_raw: Optional[str] = byte_to_str(data=encryptor.iv)
        salt_raw: Optional[str] = byte_to_str(data=encryptor.salt)

        if not iv_raw or not salt_raw:
            raise RuntimeError(
                f"IV and SALT are not allowed to be of type 'None'. iv='{iv_raw}', salt='{salt_raw}'"
            )
        iv: str = iv_raw
        salt: str = salt_raw
        pwd_hash: str = self._hasher.hash_password(
            password=str(self._entry_password.value)
        )
        self._storages.client_storage.set(key=config.CS_USER_PASSWORD_IV, value=iv)
        self._storages.client_storage.set(
            key=config.CS_USER_PASSWORD_HASH, value=pwd_hash
        )
        self._storages.client_storage.set(
            key=config.CS_USER_SALT,
            value=salt,
        )

        # Hide progress bar
        self._progress_visible(visible=False)
        self._button_clickable(clickable=True)

        # Restart login page to show the login button
        self._router.remove_route(route=config.ROUTE_LOGIN)
        self._router.add_route(
            route=config.ROUTE_LOGIN,
            content={
                "title": "Login",
                "page_content": [
                    LoginPage(
                        page=self._page,
                        storages=self._storages,
                        router=self._router,
                    ).build(),
                ],
                "execute_function": None,
                "function_args": None,
            },
        )
        self._router.go(config.ROUTE_LOGIN)

    def _login(self, e: ft.ControlEvent) -> None:
        # Give the user feedback that something happens
        self._button_clickable(clickable=False)
        self._progress_visible(visible=True)

        if not self._password_hash or not self._hasher.verify_password(
            hash=self._password_hash, password=str(self._entry_password.value)
        ):
            wrong_pwd_alert: ft.AlertDialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(value="Wrong Password!"),
                content=ft.Text(
                    value="You entered a wrong password. Please try again!",
                ),
                actions=[
                    ft.TextButton(
                        text="OK",
                        on_click=lambda e: self._page.close(wrong_pwd_alert),
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self._page.open(wrong_pwd_alert)

            # Enable the button again and hide progress bar
            self._button_clickable(clickable=True)
            self._progress_visible(visible=False)
            return

        # Set key for this session for decrypting data later
        if self._salt is None:
            raise ValueError("No salt existing. Try to reinstall app!")

        self._storages.session_storage.set(
            key=config.SS_USER_SESSION_KEY,
            value=self._hasher.derive_key(
                password=str(self._entry_password.value), salt=self._salt
            ),
        )

        # Hide progress bar on success
        self._progress_visible(visible=False)
        self._button_clickable(clickable=True)

        # Clear entries
        self._entry_password.value = ""
        if not self._user_already_exists:
            self._entry_password_confirmation.value = ""
        self._entry_password.update()
        if not self._user_already_exists:
            self._entry_password_confirmation.update()

        self._router.go(config.ROUTE_CONTACTS)

    def show_info_dialog(self) -> None:
        info_alert: ft.AlertDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(value="Correct Password!"),
            content=ft.Text(value="The passwords you entered are equal!"),
            actions=[
                ft.TextButton(
                    text="Continue",
                    on_click=lambda e: self._page.close(info_alert),
                ),
            ],
        )
        self._page.open(info_alert)

    def build(self) -> ft.Container:
        return MasterContainer(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self._entry_password,
                            *(
                                [self._entry_password_confirmation]
                                if not self._user_already_exists
                                else []
                            ),
                            self._progress_bar,
                            self._button_submit,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
        )
