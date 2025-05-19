from typing import Optional

import flet as ft  # type:ignore[import-untyped]

# Config
from env.config import config

# Func
from env.func.security import (
    byte_to_str,
    generate_iv,
    hash_password,
    str_to_byte,
    verify_password,
)

# from env.func.get_session_key import get_key_or_default


class Login(ft.Column):
    def __init__(self, page: ft.Page, contrls: list[ft.Control]) -> None:
        super().__init__()  # type:ignore

        self._page = page
        self._controls = contrls

        # Get password
        password_iv_tmp: Optional[str] = self._page.client_storage.get("password-iv")
        self.password_iv: Optional[bytes] = (
            str_to_byte(data=password_iv_tmp)
            if isinstance(password_iv_tmp, str) and password_iv_tmp
            else None
        )
        self.user_already_exists: bool = True if self.password_iv else False

        print(self.password_iv, self.user_already_exists)

        # Progress bar
        self._progress_bar = ft.ProgressBar(visible=False)

        # Create password entries
        self.password_entry: ft.TextField = ft.TextField(
            label="Password",
            text_align=ft.TextAlign.LEFT,
            on_change=self.validate,
            password=True,
            can_reveal_password=True,
            filled=True,
        )
        if (
            not self.user_already_exists
        ):  # Create a second password entry to verify the password if no iv exists
            self.password_verify_entry: ft.TextField = ft.TextField(
                label="Verify Password",
                text_align=ft.TextAlign.LEFT,
                on_change=self.validate,
                password=True,
                can_reveal_password=True,
                filled=True,
            )

        self.button_login: ft.ElevatedButton = ft.ElevatedButton(
            text=("Login" if self.user_already_exists else "Create Password"),
            width=200,
            disabled=True,
            on_click=(self.submit if self.user_already_exists else self.create_account),
        )

        # Align content
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 10
        self.expand = True

        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Image(src="assets/icon.png", width=300),
                        self.password_entry,
                        *(
                            [self.password_verify_entry]
                            if not self.user_already_exists
                            else []
                        ),
                        self._progress_bar,
                        self.button_login,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    spacing=10,
                ),
                expand=True,
                padding=40,
                alignment=ft.alignment.center,
            )
        ]

        if not self.user_already_exists:
            warning_model: ft.AlertDialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Important!"),
                content=ft.Text(
                    "Now you will be asked to create a password to encrypt your messages. "
                    "Please enter it correctly and remember it. You won't be able to decrypt the data "
                    "if you forget or loose your password."
                ),
                actions=[
                    ft.TextButton(
                        "I understand!",
                        on_click=lambda e: self._page.close(warning_model),
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self._page.open(warning_model)

    def show_progress(self) -> None:
        self._progress_bar.visible = True
        self._page.update()  # type:ignore

    def hide_progress(self) -> None:
        self._progress_bar.visible = False
        self._page.update()  # type:ignore

    def validate(self, e: ft.ControlEvent) -> None:
        # Disable button if nothing inserted
        self.button_login.disabled = (
            False
            if all(
                [
                    self.password_entry.value,
                    *(
                        [self.password_verify_entry.value]
                        if not self.user_already_exists
                        else []
                    ),
                ]
            )
            else True
        )
        self._page.update()  # type:ignore

    def create_account(self, e: ft.ControlEvent) -> None:
        # Deactivate the login button to avoid multiple processes running at the same time
        self.button_login.disabled = True
        self.button_login.update()  # type:ignore

        if self.password_entry.value != self.password_verify_entry.value:
            verify_pwd_model: ft.AlertDialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text(
                    "The passwords you entered are not equal! Please reenter them."
                ),
                actions=[
                    ft.TextButton(
                        "OK", on_click=lambda e: self._page.close(verify_pwd_model)
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self._page.open(verify_pwd_model)

            # Reactivate the login button to make sure the user can input stuff
            self.button_login.disabled = False
            self.button_login.update()  # type:ignore
            self.hide_progress()
            return

        self.show_progress()  # type:ignore  # Show progress bar

        iv: str = byte_to_str(data=generate_iv())
        pwd_hash: str = hash_password(password=str(self.password_entry.value))
        self._page.client_storage.set(key=config.CS_PASSWORD_IV, value=iv)
        self._page.client_storage.set(key=config.CS_PASSWORD_HASH, value=pwd_hash)

        self.hide_progress()  # type:ignore  # Hide progress bar

        print(f"Stored {iv=} and {pwd_hash=}")
        self._page.clean()
        self._page.add(Login(page=self._page, contrls=self._controls))

    def submit(self, e: ft.ControlEvent) -> None:
        # Deactivate the login button to avoid multiple processes running at the same time
        self.button_login.disabled = True
        self.button_login.update()  # type:ignore

        self.show_progress()  # type:ignore  # Show progress bar

        password: str = str(self.password_entry.value)

        stored_hash: Optional[str] = self._page.client_storage.get(
            config.CS_PASSWORD_HASH
        )
        if not stored_hash or not verify_password(
            hash=stored_hash, password=str(self.password_entry.value)
        ):
            wrng_pwd_alert: ft.AlertDialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please try again!"),
                content=ft.Text("You entered a wrong password!"),
                actions=[
                    ft.TextButton(
                        "OK", on_click=lambda e: self._page.close(wrng_pwd_alert)
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self._page.open(wrng_pwd_alert)

            # Reactivate the login button to make sure the user can input stuff
            self.button_login.disabled = False
            self.button_login.update()  # type:ignore
            self.hide_progress()
            return

        self.hide_progress()  # type:ignore  # Hide progress bar on success

        print(f"Logged in with password '{password}'")
        self._page.clean()
        self._page.add(*self._controls)
