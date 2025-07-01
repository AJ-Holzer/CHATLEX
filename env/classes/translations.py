import json
import os
from typing import Any, Optional, cast

import flet as ft  # type:ignore[import-untyped]

from env.classes.storages import Storages
from env.config import config
from env.func.route_normalization import normalize_route
from env.typing.languages import (CONTROL_STATE_KEYS, TRANSLATION_CONTROLS,
                                  ControlAddingData, ControlLanguageData,
                                  ControlStates, Language, LanguageData)


# TODO: Use I18n instead!
class Translator:
    def __init__(
        self,
        page: ft.Page,
        storages: Storages,
    ) -> None:
        self._page: ft.Page = page
        self._storages: Storages = storages

        # Set current language
        self._current_language: Language = self._storages.client_storage.get(
            key=config.CS_LANGUAGE,
            default=config.LANGUAGE_DEFAULT,
        )

        # Create dict for accessing all controls
        self._all_controls: dict[str, TRANSLATION_CONTROLS] = {}

        # Define and load language data
        self._current_language_data: dict[str, LanguageData] = {}
        self._load_language_data()

    def _load_language_data(self) -> None:
        # Define file path
        file_path: str = os.path.join(
            config.FOLDER_LANGUAGES, f"{self._current_language.value}.json"
        )

        # Check if file exists
        if not os.path.exists(path=file_path):
            raise FileNotFoundError(f"Language file '{file_path}' does not exist!")

        # Load language data
        try:
            with open(file=file_path, mode="r", encoding="UTF-8") as f:
                self._current_language_data = json.load(f)
        except Exception as e:
            print(
                f"Exception has occurred while loading language file '{file_path}': {e}"
            )

    def _normalize_route(self, route: str, control_name: str) -> str:
        return normalize_route(path=f"{route}/{control_name}")

    def _set_control_args(
        self,
        control_route: str,
        states: Optional[ControlStates],
        **replacements: Any,
    ) -> None:
        # Get language data for control
        language_data: Optional[LanguageData] = self._current_language_data.get(
            control_route
        )

        # Check if language data provided
        if not language_data:
            raise ValueError(
                f"No language data provided for control with route '{control_route}'!"
            )

        # Create control language data dictionary
        control_language_data: ControlLanguageData = {
            "value": None,
            "label": None,
            "text": None,
            "helper_text": None,
            "error_text": None,
            "tooltip": None,
        }

        # Check if states are given and update control language data dictionary
        if states is not None:
            # Get control language data with given states
            for state_key, state_value in states.items():
                if state_key not in ControlStates.__annotations__:
                    raise ValueError(
                        f"State key '{state_key}' is not valid! Use one of these instead: "
                        f"{', '.join(ControlStates.__annotations__.keys())}"
                    )

                # Cast key and value to avoid typing error
                typed_key: CONTROL_STATE_KEYS = cast(
                    CONTROL_STATE_KEYS,
                    state_key,
                )
                typed_value: CONTROL_STATE_KEYS = cast(
                    CONTROL_STATE_KEYS,
                    state_value,
                )

                # Update control language data dictionary
                try:
                    control_language_data[typed_key] = language_data[typed_key][
                        (typed_value if state_value is not None else "init")
                    ]
                except Exception as e:
                    print(
                        f"Exception has occurred while updating the control language data with states='{states}': {e}"
                    )
                    return

        # Fallback to 'init' state
        else:
            for key in control_language_data.keys():
                typed_fallback_key: CONTROL_STATE_KEYS = cast(CONTROL_STATE_KEYS, key)
                control_language_data[typed_fallback_key] = language_data.get(
                    typed_fallback_key, {}
                ).get("init")

        # Get control
        control: Optional[TRANSLATION_CONTROLS] = self._all_controls.get(control_route)

        # Check if control provided
        if not control:
            raise ValueError(f"No control provided for route '{control_route}'!")

        # Set args
        try:
            for attr, value in control_language_data.items():
                # Check if control has the attr
                if not hasattr(control, "attr"):
                    continue

                # Check if value is 'None'
                if value is None:
                    continue

                # Set the attr to 'None' if (value == '<DO_REPLACE>')
                if value == "<DO_REPLACE>":
                    setattr(control, attr, None)
                    continue

                # Set attribute
                setattr(control, attr, str(value).format(**replacements))
        except Exception as e:
            print(
                f"There was an error while setting the attribute for control with route '{control_route}'! Error: {e}"
            )
            return

    def _update_all_controls(self) -> None:
        for control in self._all_controls.values():
            control.update()

    def add_control(
        self,
        route: str,
        control_name: str,
        control: ft.Control,
    ) -> None:
        # Check if control is valid
        if not isinstance(control, TRANSLATION_CONTROLS):
            raise ValueError(f"Control '{control}' is not valid to add to translator!")

        # Normalize route
        normalized_route: str = self._normalize_route(
            route=route,
            control_name=control_name,
        )

        # Add control to dictionary
        self._all_controls[normalized_route] = control

    def add_controls(
        self,
        route: str,
        control_adding_data: list[ControlAddingData],
    ) -> None:
        for control_data in control_adding_data:
            self.add_control(
                route=route,
                control_name=control_data["control_name"],
                control=control_data["control"],
            )

    def wrap_control(
        self,
        route: str,
        control_name: str,
        control: ft.Control,
        **replacements: Any,
    ) -> ft.Control:
        # Check if control is valid
        if not isinstance(control, TRANSLATION_CONTROLS):
            raise ValueError(
                f"Control '{control}' is not valid to be added to translator!"
            )

        # Add control to cache
        self.add_control(route=route, control_name=control_name, control=control)

        # Set args
        self._set_control_args(
            control_route=self._normalize_route(route=route, control_name=control_name),
            states=None,
            **replacements,
        )

        return control

    def update_control_state(
        self,
        route: str,
        control_name: str,
        states: ControlStates,
    ) -> None:
        # Normalize route
        normalized_route: str = self._normalize_route(
            route=route,
            control_name=control_name,
        )

        # Raise value error if route does not exist
        if normalized_route not in self._all_controls:
            raise ValueError(f"Route '{normalized_route}' does not exist!")

        # Get control
        control: ft.Control = self._all_controls[normalized_route]

        # Get data
        control_language_data: Optional[LanguageData] = self._current_language_data.get(
            normalized_route,
        )

        # Print todo if no data for route exists
        if control_language_data is None:
            print(
                f"ToDo: Add text for widget '{normalized_route}' with states='{states}' and language='{self._current_language}'"
            )
            return

        # Update text with given state
        self._set_control_args(
            control_route=normalized_route,
            states=states,
        )

        # Update control
        control.update()

    def set_language(self, language: Language) -> None:
        # Update current language
        self._current_language = language

        # Walk through all controls and set their texts
        for control_route in self._all_controls:
            self._set_control_args(control_route=control_route, states=None)

        # Update controls
        self._update_all_controls()
