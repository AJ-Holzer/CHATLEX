import flet as ft  # type:ignore[import-untyped]
import random  # TODO: Remove when tests are done!

# Func
from env.func.get_session_key import get_key_or_default

# Config
from env.config import config

# Classes
from env.classes.widgets import Contact
from env.classes.faker import Faker

fake = Faker()

class UI(ft.Tabs):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()  # type:ignore

        self._page: ft.Page = page
        self.default_font_size: int = get_key_or_default(page=self._page, default=config.FONT_SIZE_DEFAULT, key_name="font-size")
        self.default_font: str = get_key_or_default(page=self._page, default=config.FONT_FAMILY_DEFAULT, key_name="font-family")
        self.all_text_elements: list[tuple[ft.Text, int] | tuple[ft.ElevatedButton, int] | tuple[ft.TextButton, int]] = []

        # Tabs
        # self._label_color: ft.ColorValue = ft.Colors.PURPLE_400
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
        # self.indicator_color = ft.Colors.PURPLE_100
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

        def update_font_size(e: ft.ControlEvent) -> None:
            new_size: int = int(e.control.value)  # type:ignore
            self._page.client_storage.set(key="font-size", value=new_size)
            self.default_font_size = new_size
            print(f"New font size: {self._page.client_storage.get('font-size')}")

            for element, deviation in self.all_text_elements:
                updated_size = new_size + deviation

                if isinstance(element, ft.Text):
                    element.size = updated_size

                elif isinstance(element, ft.ElevatedButton):
                    element.style = ft.ButtonStyle(
                        text_style=ft.TextStyle(size=updated_size)
                    )

                # elif isinstance(element, ft.TextButton):
                #     element.style = ft.ButtonStyle(
                #         color=element.style.color if element.style and isinstance(element.style, ft.ButtonStyle) else None,
                #         text_style=ft.TextStyle(size=updated_size)
                #     )
                
                else:
                    element.style = ft.ButtonStyle(
                        color=element.style.color if element.style else None,
                        text_style=ft.TextStyle(size=updated_size)
                    )

                element.update()
                
        def update_font_family(e: ft.ControlEvent) -> None:
            new_font_family: str = str(e.control.value)  # type:ignore
            self._page.client_storage.set("font-family", new_font_family)  # type:ignore
            print(f"New font: {self._page.client_storage.get("font-family")}")
            
            for element, _ in self.all_text_elements:
                if isinstance(element, ft.Text):
                    element.font_family = new_font_family
                elif isinstance(element, ft.ElevatedButton):
                    element.style = ft.ButtonStyle(
                        text_style=ft.TextStyle(font_family=new_font_family)
                    )
                # elif isinstance(element, ft.TextButton):
                #     element.style = ft.ButtonStyle(
                #         color=element.style.color if element.style and isinstance(element.style, ft.ButtonStyle) else None,
                #         text_style=ft.TextStyle(size=element.style.text_style.size, font_family=new_font_family)
                #     )
                else:
                    element.style = ft.ButtonStyle(
                        color=element.style.color if element.style else None,
                        text_style=ft.TextStyle(size=self.default_font_size, font_family=new_font_family)
                    )
                
                element.update()


        font_size_label: ft.Text = ft.Text(
            "Font size",
            style=ft.TextStyle(font_family=self.default_font, size=self.default_font_size, color=ft.Colors.ON_SURFACE_VARIANT)
        )

        font_size_slider: ft.Slider = ft.Slider(
            min=config.FONT_MIN_SIZE,
            max=config.FONT_MAX_SIZE,
            divisions=abs(config.FONT_MAX_SIZE - config.FONT_MIN_SIZE),
            value=self.default_font_size,
            label="{value}",
            active_color=ft.Colors.PURPLE_700,
            # on_change=update_font_size
            on_change_end=update_font_size
        )
        
        font_family_dropdown: ft.Dropdown = ft.Dropdown(
            value=self.default_font,
            options=[ft.DropdownOption(key=font_name) for font_name in self._page.fonts.keys()] if self._page.fonts else None,  # type:ignore
            on_change=update_font_family
        )
        
        self.all_text_elements.append((font_size_label, 0))

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
        
        contacts: list[Contact] = [Contact(username=fake.name, size=self.default_font_size, contact_uid="10000", tab_change_function=self.switch_to_tab, chat_tab=self._chat_tab, contact_info_tab=self._contact_info_tab, is_online=random.choice([True, False])) for _ in range(100)]

        contacts_lv: ft.ReorderableListView = ft.ReorderableListView(
            controls=[contact.build() for contact in contacts],
            expand=True
        )

        self.all_text_elements.extend([(text_widget.text_widget, 0) for text_widget in contacts])

        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=20,
                controls=[contacts_lv]
            )
        )

    def chat_page(self) -> ft.Container:
        # https://flet.dev/docs/controls/markdown                        # For showing message
        # https://flet.dev/docs/controls/textfield                       # For msg input
        # https://flet.dev/docs/controls/textfield#multiline-textfields  # For msg input
        # https://flet.dev/docs/cookbook/large-lists                     # Use for displaying many message bubbles --> runs smoothly
        # https://flet.dev/docs/cookbook/encrypting-sensitive-data       # Maybe use this encryption method if aes-256 isn't available everywhere
        return ft.Container()

    def contact_info_page(self) -> ft.Container:
        # https://flet.dev/docs/controls/circleavatar                    # Showing the profile image of the current user
        return ft.Container()

    def about_page(self) -> ft.Container:
        header_about: ft.Text = ft.Text("About This App", font_family=self.default_font, style=ft.TextStyle(size=self.default_font_size + 15))
        description_about: ft.Text = ft.Text(
            "This application was built using Python and the Flet framework.\n"
            "It aims to provide a clean, efficient, and modern user experience "
            "while showcasing the power of security and sleek UI.",
            style=ft.TextStyle(font_family=self.default_font, size=self.default_font_size, color=ft.Colors.ON_SURFACE_VARIANT),
        )
        divider: ft.Divider = ft.Divider(height=1, color=ft.Colors.PURPLE_200)
        header_developer_info: ft.Text = ft.Text(
            "Developer Info",
            style=ft.TextStyle(font_family=self.default_font, size=self.default_font_size + 5, weight=ft.FontWeight.BOLD),
        )
        description_developer_info: ft.Text = ft.Text(
            "Created by AJ-Holzer\n"
            "Passionate about robotics, secure communication systems, and Python development.",
            style=ft.TextStyle(font_family=self.default_font, size=self.default_font_size),
        )
        website_button: ft.TextButton = ft.TextButton(
            "Visit: ajservers.site",
            url="https://ajservers.site",
            # style=ft.ButtonStyle(color=ft.Colors.PURPLE, text_style=ft.TextStyle(font_family=self.default_font, size=self.default_font_size))
        )
        
        self.all_text_elements.extend([
            (header_about              , 15),
            (description_about         ,  0),
            (header_developer_info     ,  5),
            (description_developer_info,  0),
        ])
        self.all_text_elements.append((website_button, 0))
        
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
                controls=[
                    header_about,
                    description_about,
                    divider,
                    header_developer_info,
                    description_developer_info,
                    website_button
                ],
            ),
        )

