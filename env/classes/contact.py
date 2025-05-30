import uuid
from typing import Optional

# TODO: Import database!


class Contact:
    def __init__(self, contact_uuid: str) -> None:
        self._uuid: str = (
            contact_uuid  # TODO: Check if uuid exists. Raise error if not!
        )

        # Get user data
        self._username: str  # TODO: Add username
        self._description: Optional[str]  # TODO: Add description
        self._initials: str = "".join(
            word.strip()[0] for word in self._username.split(sep=" ", maxsplit=1)
        )
        self._onion_address: str  # TODO: Add address

    def _create_uuid(self) -> str:
        return uuid.uuid4().hex

    @property
    def username(self) -> str:
        return self._username

    @property
    def initials(self) -> str:
        return self._initials

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def onion_address(self) -> str:
        return self._onion_address
