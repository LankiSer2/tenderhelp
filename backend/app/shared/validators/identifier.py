from enum import StrEnum


class IdentifierType(StrEnum):
    INN = "INN"
    OGRN = "OGRN"
    UNKNOWN = "UNKNOWN"


def _digits_only(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())


def _inn_checksum_valid(inn: str) -> bool:
    if len(inn) == 10:
        coeffs = (2, 4, 10, 3, 5, 9, 4, 6, 8)
        control = sum(c * int(d) for c, d in zip(coeffs, inn[:9], strict=True)) % 11 % 10
        return control == int(inn[9])

    if len(inn) == 12:
        coeffs_11 = (7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        coeffs_12 = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        control_11 = sum(c * int(d) for c, d in zip(coeffs_11, inn[:10], strict=True)) % 11 % 10
        control_12 = sum(c * int(d) for c, d in zip(coeffs_12, inn[:11], strict=True)) % 11 % 10
        return control_11 == int(inn[10]) and control_12 == int(inn[11])

    return False


def _ogrn_checksum_valid(ogrn: str) -> bool:
    if len(ogrn) == 13:
        return int(ogrn[:12]) % 11 % 10 == int(ogrn[12])
    if len(ogrn) == 15:
        return int(ogrn[:14]) % 13 % 10 == int(ogrn[14])
    return False


def detect_identifier_type(raw: str) -> IdentifierType:
    value = _digits_only(raw)
    if len(value) in (10, 12) and _inn_checksum_valid(value):
        return IdentifierType.INN
    if len(value) in (13, 15) and _ogrn_checksum_valid(value):
        return IdentifierType.OGRN
    if len(value) in (10, 12):
        return IdentifierType.INN
    if len(value) in (13, 15):
        return IdentifierType.OGRN
    return IdentifierType.UNKNOWN


def normalize_identifier(raw: str) -> str:
    return _digits_only(raw)
