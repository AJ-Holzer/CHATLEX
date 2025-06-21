from typing import Optional

import flet as ft  # type:ignore[import-untyped]

from env.app.widgets.container import MasterContainer
from env.classes.hashing import ArgonHasher
from env.classes.paths import paths
from env.classes.phone_sensors import ShakeDetector
from env.classes.router import AppRouter
from env.classes.storages import Storages
from env.config import config
from env.func.converter import byte_to_str, str_to_byte
from env.func.generations import generate_iv, generate_salt


class LoginPage:
    def __init__(
        self,
        page: ft.Page,
        storages: Storages,
        router: AppRouter,
        shake_detector: ShakeDetector,
    ) -> None:
        # Initialize page
        self._page: ft.Page = page
        self._storages: Storages = storages
        self._router: AppRouter = router
        self._shake_detector: ShakeDetector = shake_detector

        # User stuff
        self._user_already_exists: bool = bool(
            self._storages.client_storage.get(key=config.CS_USER_PASSWORD_HASH)
        ) and bool(self._storages.client_storage.get(key=config.CS_USER_PASSWORD_IV))

        # Password stuff
        self._password_hash: Optional[str] = storages.client_storage.get(
            key=config.CS_USER_PASSWORD_HASH
        )

        # Get salt
        self._salt: bytes
        stored_salt: Optional[str] = self._storages.client_storage.get(
            key=config.CS_USER_SALT,
            default=None,
        )
        if stored_salt is None:
            self._salt = generate_salt(salt_length=config.SALT_LENGTH)
        elif len(str_to_byte(stored_salt)) == config.SALT_LENGTH:
            self._salt = str_to_byte(stored_salt)
        else:
            raise ValueError(
                f"Stored salt '{str(stored_salt)}' with length={len(stored_salt)} is invalid! Try reinstalling the app!"
            )

        # Get IV
        self._iv: bytes
        stored_iv: Optional[str] = self._storages.client_storage.get(
            key=config.CS_USER_PASSWORD_IV,
            default=None,
        )
        if stored_iv is None:
            self._iv = generate_iv()
        elif len(str_to_byte(stored_iv)) == 16:
            self._iv = str_to_byte(stored_iv)
        else:
            raise ValueError(
                f"Stored salt '{str(stored_salt)}' is invalid! Try reinstalling the app!"
            )

        # Entries
        self._entry_password: ft.TextField = ft.TextField(
            label="Password",
            password=True,
            on_change=self._validate,
            autofocus=True,
            autocorrect=False,
        )
        if not self._user_already_exists:
            self._entry_password_confirmation: ft.TextField = ft.TextField(
                label="Confirm Password",
                password=True,
                on_change=self._validate,
                autocorrect=False,
            )

        # Buttons
        self._button_submit: ft.ElevatedButton = ft.ElevatedButton(
            text="Login" if self._user_already_exists else "Create Account",
            on_click=self._login if self._user_already_exists else self._create_account,
            disabled=True,
        )

        # Progress bar
        self._progress_bar: ft.ProgressBar = ft.ProgressBar(visible=False)

        # Image
        self._app_logo: ft.Image = ft.Image(
            src=paths.join_with_base_path("assets/icon.png"),
            width=300,
        )

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

    def _get_argon2_hasher(self) -> ArgonHasher:
        return ArgonHasher(storages=self._storages)

    def _create_account(self, e: ft.ControlEvent) -> None:
        # Initialize Argon2 hasher
        argon_hasher: ArgonHasher = self._get_argon2_hasher()

        # Give the user feedback that something is happening
        self._button_clickable(clickable=False)
        self._progress_visible(visible=True)

        if self._entry_password.value != self._entry_password_confirmation.value:
            pwd_not_equal_alert: ft.AlertDialog = ft.AlertDialog(
                modal=False,
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

            # Show info alert and wait until it is closed before proceeding

        info_alert_closed: bool = False
        cancelled: bool = False

        def on_info_alert_close(e: ft.ControlEvent) -> None:
            nonlocal info_alert_closed
            info_alert_closed = True
            self._page.close(info_alert)

        def on_cancel(e: ft.ControlEvent) -> None:
            nonlocal cancelled, info_alert_closed
            self._progress_visible(visible=False)
            self._button_clickable(clickable=True)
            self._page.close(info_alert)
            info_alert_closed = True
            cancelled = True

        info_alert: ft.AlertDialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(value="Important Information!"),
            content=ft.Text(
                value="Are you sure you remember the password? You can not decrypt the data if you forget it!"
            ),
            actions=[
                ft.TextButton(
                    text="NO",
                    on_click=on_cancel,
                ),
                ft.TextButton(
                    text="YES",
                    on_click=on_info_alert_close,
                ),
            ],
        )
        self._page.open(info_alert)

        # Wait for the dialog to be closed
        while not info_alert_closed:
            self._page.update()  # type:ignore
        print("Closed")

        # Check if user cancelled the action
        if cancelled:
            print("Cancelled")
            return

        # Show progress bar to indicate something is happening
        self._progress_visible(visible=True)

        # Generate password hash
        pwd_hash: str = argon_hasher.hash_password(
            password=str(self._entry_password.value)
        )

        # Store IV
        self._storages.client_storage.set(
            key=config.CS_USER_PASSWORD_IV,
            value=byte_to_str(self._iv),
        )
        # Store password hash
        self._storages.client_storage.set(
            key=config.CS_USER_PASSWORD_HASH,
            value=pwd_hash,
        )
        # Store salt
        self._storages.client_storage.set(
            key=config.CS_USER_SALT,
            value=byte_to_str(self._salt),
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
                        shake_detector=self._shake_detector,
                    ).build(),
                ],
                "execute_function": None,
                "function_args": None,
            },
        )
        self._router.go(config.ROUTE_LOGIN)

    def _login(self, e: ft.ControlEvent) -> None:
        # Initialize Argon2 hasher
        argon_hasher: ArgonHasher = self._get_argon2_hasher()

        # Give the user feedback that something happens
        self._button_clickable(clickable=False)
        self._progress_visible(visible=True)

        if not self._password_hash or not argon_hasher.verify_password(
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
        if not self._salt:
            raise ValueError(
                f"No salt existing. Salt='{self._salt}' Try to reinstall app!"
            )

        # Store derived session storage key to encrypt and decrypt data
        self._storages.session_storage.set(
            key=config.SS_USER_SESSION_KEY,
            value=byte_to_str(
                data=argon_hasher.derive_key(
                    password=str(self._entry_password.value),
                    salt=self._salt,
                )
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

        # Enable shake detection if setting set to 'True'
        if self._storages.client_storage.get(
            key=config.CS_SHAKE_DETECTION, default=config.SHAKE_ENABLED_DEFAULT
        ):
            self._shake_detector.enable()

        self._router.go(config.ROUTE_CONTACTS)

    def initialize(self) -> None:
        # Disable shake detector when showing login page to avoid logging out
        # when not logged in
        self._shake_detector.disable()

    def build(self) -> ft.Container:
        return MasterContainer(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self._app_logo,
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
