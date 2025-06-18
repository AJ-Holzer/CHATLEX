from typing import Optional

from env.typing.dicts import ContactData


class Contact:
    def __init__(self, contact_data: ContactData) -> None:
        self._contact_data: ContactData = contact_data
        self._is_online: bool = False

        # Get user data
        self._initials: str = self._get_initials()

    def _get_initials(self) -> str:
        return "".join(
            word.strip()[0]
            for word in self._contact_data["username"].split(sep=" ", maxsplit=1)
        )

    @property
    def contact_uuid(self) -> str:
        return self._contact_data["contact_uuid"]

    @property
    def order_index(self) -> int:
        if self._contact_data["order_index"] is None:
            raise ValueError(
                f"No order index provided for contact {self._contact_data['contact_uuid']}!"
            )

        return self._contact_data["order_index"]

    @order_index.setter
    def order_index(self, value: int) -> None:
        self._contact_data["order_index"] = value

    @property
    def initials(self) -> str:
        return self._initials

    @property
    def contact_data(self) -> ContactData:
        return self._contact_data

    @property
    def username(self) -> str:
        return self._contact_data["username"]

    @username.setter
    def username(self, value: str) -> None:
        self._contact_data["username"] = value
        self._initials = self._get_initials()

    @property
    def description(self) -> Optional[str]:
        return self._contact_data["description"]

    @description.setter
    def description(self, value: str) -> None:
        self._contact_data["description"] = value

    @property
    def onion_address(self) -> str:
        return self._contact_data["onion_address"]

    @onion_address.setter
    def onion_address(self, value: str) -> None:
        self._contact_data["onion_address"] = value

    @property
    def is_online(self) -> bool:
        return self._is_online

    @is_online.setter
    def is_online(self, value: bool) -> None:
        self._is_online = value

    @property
    def is_muted(self) -> bool:
        return self._contact_data["muted"]

    @is_muted.setter
    def is_muted(self, value: bool) -> None:
        self._contact_data["muted"] = value

    @property
    def is_blocked(self) -> bool:
        return self._contact_data["blocked"]

    @is_blocked.setter
    def is_blocked(self, value: bool) -> None:
        self._contact_data["blocked"] = value
