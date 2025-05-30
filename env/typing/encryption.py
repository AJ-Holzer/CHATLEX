from typing import Optional, TypedDict

from nacl.signing import SigningKey, VerifyKey


class MasterKeys(TypedDict):
    private_key: Optional[SigningKey]
    public_key: Optional[VerifyKey]


class SignedOnionData(TypedDict):
    onion: str
    timestamp: float
    expires: float
    signed_by: str
    signature: str
