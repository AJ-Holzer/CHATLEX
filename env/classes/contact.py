from typing import Optional

from env.typing.dicts import ContactData

# TODO: Import database!


class Contact:
    def __init__(self, contact_data: ContactData) -> None:
        self._contact_data: ContactData = contact_data
        self._is_online: bool = False

        # Get user data
        self._initials: str = "".join(
            word.strip()[0]
            for word in self._contact_data["username"].split(sep=" ", maxsplit=1)
        )

    @property
    def username(self) -> str:
        return self._contact_data["username"]

    @property
    def description(self) -> Optional[str]:
        return self._contact_data["description"]

    @property
    def contact_uuid(self) -> str:
        return self._contact_data["contact_uuid"]

    @property
    def onion_address(self) -> str:
        return self._contact_data["onion_address"]

    @property
    def initials(self) -> str:
        return self._initials

    @property
    def is_online(self) -> bool:
        return self._is_online

    @is_online.setter
    def is_online(self, value: bool) -> None:
        self._is_online = value
