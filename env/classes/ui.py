import flet as ft  # type:ignore[import-untyped]
import random  # TODO: Remove when tests are done!

# Func
from env.func.get_session_key import get_key_or_default

# Config
from env.config import config

# Classes
from env.classes.widgets import Contact, CText
from env.classes.faker import Faker

fake = Faker()

class UI(ft.Tabs):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()  # type:ignore

        self._page: ft.Page = page
        self.default_font_size: int = get_key_or_default(page=self._page, default=config.FONT_SIZE_DEFAULT, key_name="font-size")
        self.default_font: str = get_key_or_default(page=self._page, default=config.FONT_FAMILY_DEFAULT, key_name="font-family")

        # Tabs
        self._chat_tab: ft.Tab = ft.Tab(
            icon=ft.Icon(name=ft.Icons.CHAT_OUTLINED, size=30),
            content=self.chat_page()
        )
        self._contact_info_tab: ft.Tab = ft.Tab(
            icon=ft.Icon(name=ft.Icons.PERSON, size=30),
            content=self.contact_info_page()
        )
        self._settings_tab: ft.Tab = ft.Tab(
            icon=ft.Icon(name=ft.Icons.SETTINGS_OUTLINED, size=30),
            content=self.settings_page()
        )
        self._contacts_tab: ft.Tab = ft.Tab(
            icon=ft.Icon(name=ft.Icons.PEOPLE, size=30),
            content=self.contacts_page()
        )
        self._about_tab: ft.Tab = ft.Tab(
            icon=ft.Icon(name=ft.Icons.INFO_OUTLINE_ROUNDED, size=30),
            content=self.about_page()
        )
        self.tabs = [
            self._settings_tab,
            self._contacts_tab,
            self._chat_tab,
            self._contact_info_tab,
            self._about_tab,
        ]
        self.tab_alignment = ft.TabAlignment.CENTER
        self.animation_duration = 300
        self.expand = True
        self.selected_index = 1
        
        # Create shortcut to quickly go back to contacts page
        self._page.on_route_change
        
    def switch_to_tab(self, selected_index: int) -> None:
        self.selected_index = selected_index
        self.update()

    def settings_page(self) -> ft.Container:
        # https://flet.dev/docs/controls/progressbar                # When creating backup or something like that?
        # https://flet.dev/docs/controls/cupertinoswitch            # When making some settings for yes/no
        # https://flet.dev/docs/controls/switch                     # Or use this switch for yes/no settings
        # https://flet.dev/docs/controls/radio                      # For multiple choices
        # https://flet.dev/docs/controls/shakedetector              # When the phone will be shaken, just exit the app and lock it
        # https://flet.dev/docs/cookbook/session-storage            # Use session storage for storing settings --> Use Client-Storage instead (saves the settings)
        # https://flet.dev/docs/reference/colors                    # Use custom accent color
        # https://flet.dev/docs/controls/dropdown                   # Drop-down menu for language and font settings

        def on_setting_changed(e: ft.ControlEvent) -> None:
            self._page.open(ft.SnackBar(CText(page=self._page, value="Restart application to apply changes!"), duration=2000))
            self._page.update()  # type:ignore
            
            # Update client storage
            self._page.client_storage.set(config.CS_FONT_SIZE, font_size_slider.value)
            self._page.client_storage.set(config.CS_FONT_FAMILY, font_family_dropdown.value)

        font_size_label: ft.Text = CText(page=self._page, value="Font Settings", style=ft.TextStyle(font_family=self.default_font, size=self.default_font_size))

        font_size_slider: ft.Slider = ft.Slider(
            min=config.FONT_MIN_SIZE,
            max=config.FONT_MAX_SIZE,
            divisions=abs(config.FONT_MAX_SIZE - config.FONT_MIN_SIZE),
            value=self.default_font_size,
            label="{value}",
            on_change_end=on_setting_changed,
        )
        
        font_family_dropdown: ft.Dropdown = ft.Dropdown(
            value=self.default_font,
            options=[ft.DropdownOption(key=font_name) for font_name in self._page.fonts.keys()] if self._page.fonts else None,  # type:ignore
            on_change=on_setting_changed,
        )

        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    font_size_label,
                    font_size_slider,
                    font_family_dropdown
                ]
            )
        )

    def contacts_page(self) -> ft.Container:
        # https://flet.dev/docs/controls/circleavatar                    # Showing the profile image of the users
        # https://flet.dev/docs/controls/cupertinotextfield              # For adding contacts
        # https://flet.dev/docs/reference/types/badge                    # Use to show unread messages (number)
        # https://flet.dev/docs/cookbook/large-lists                     # Use for displaying many contacts --> runs smoothly

        # <<--- TESTING PURPOSE START --->> #
        # TODO: Retrieve contacts from db when initialized!
        contacts: list[Contact] = [Contact(page=self._page, username=fake.name, contact_uid="10000", tab_change_function=self.switch_to_tab, chat_tab=self._chat_tab, contact_info_tab=self._contact_info_tab, is_online=random.choice([True, False])) for _ in range(100)]
        contacts_lv: ft.ReorderableListView = ft.ReorderableListView(
            controls=[contact.build() for contact in contacts],
            expand=True
        )
        # <<--- TESTING PURPOSE END --->> #

        return ft.Container(
            content=ft.Column(
                controls=[contacts_lv],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=20,
                expand=True,
            ),
            padding=20,
            expand=True,
        )

    def chat_page(self) -> ft.Container:
        # https://flet.dev/docs/controls/markdown                        # For showing message
        # https://flet.dev/docs/controls/textfield                       # For msg input
        # https://flet.dev/docs/controls/textfield#multiline-textfields  # For msg input
        # https://flet.dev/docs/cookbook/large-lists                     # Use for displaying many message bubbles --> runs smoothly
        # https://flet.dev/docs/cookbook/encrypting-sensitive-data       # Maybe use this encryption method if aes-256 isn't available everywhere

        text_hint: ft.Text = CText(page=self._page, value="Select a contact to chat!", font_family=self.default_font, style=ft.TextStyle(size=self.default_font_size + 0))
        
        return ft.Container(
            ft.Column(
                controls=[text_hint],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            padding=40,
            expand=True,
        )

    def contact_info_page(self) -> ft.Container:
        # https://flet.dev/docs/controls/circleavatar                    # Showing the profile image of the current user

        text_hint: ft.Text = CText(page=self._page, value="Select a contact to view Info!", font_family=self.default_font, style=ft.TextStyle(size=self.default_font_size + 0))

        return ft.Container(
            ft.Column(
                controls=[text_hint],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            padding=40,
            expand=True,
        )

    def about_page(self) -> ft.Container:
        header_about: ft.Text = CText(page=self._page, value="About This App", size_deviation=15, font_family=self.default_font)
        description_about: ft.Text = CText(
            page=self._page,
            value=(
            "This application was built using Python and the Flet framework.\n"
            "It aims to provide a clean, efficient, and modern user experience "
            "while showcasing the power of security and sleek UI."),
            style=ft.TextStyle(font_family=self.default_font, size=self.default_font_size),
        )
        divider: ft.Divider = ft.Divider(height=1)
        header_developer_info: ft.Text = CText(
            page=self._page,
            value="Developer Info",
            size_deviation=5,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )
        description_developer_info: ft.Text = CText(
            page=self._page,
            value="Created by ",
            spans=[
            ft.TextSpan(
                "AJ-Holzer",
                style=ft.TextStyle(weight=ft.FontWeight.BOLD)
            ),
            ft.TextSpan(
                "\nPassionate about robotics, secure communication systems, and Python development."
            ),
            ],
            style=ft.TextStyle(font_family=self.default_font, size=self.default_font_size),
        )
        website_button: ft.TextButton = ft.TextButton(
            "Check out my website",
            url="https://ajservers.site",
            style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                font_family=self.default_font,
                size=self.default_font_size,
            )
            )
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    header_about,
                    description_about,
                    divider,
                    header_developer_info,
                    description_developer_info,
                    website_button
                ],
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
                expand=True,
            ),
            expand=True,
            padding=20,
        )

