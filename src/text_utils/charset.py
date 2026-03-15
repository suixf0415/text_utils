"""Character encoding detection utilities."""

from typing import Dict, List, Optional, Tuple

ENCODINGS: List[str] = [
    "utf-8",
    "gbk",
    "gb2312",
    "big5",
    "iso-8859-1",
    "iso-8859-2",
    "iso-8859-9",
    "iso-8859-10",
    "windows-1252",
    "shift_jis",
    "euc-kr",
    "iso-8859-5",
    "iso-8859-7",
    "iso-8859-8",
    "koi8-r",
    "cp866",
    "cp1251",
]


def detect_encoding(data: bytes) -> Tuple[Optional[str], Dict[str, float]]:
    """Detect the encoding of byte data.

    Args:
        data: Input bytes to detect encoding for

    Returns:
        Tuple of (detected_encoding, confidence_dict)
    """
    if not data:
        return None, {}

    results: Dict[str, float] = {}

    results["utf-8"] = check_utf8(data)

    if results["utf-8"] == 1.0:
        return "utf-8", results

    results["gbk"] = check_gb_series(data, "gbk")
    results["gb2312"] = check_gb_series(data, "gb2312")
    results["big5"] = check_big5(data)

    results["shift_jis"] = check_shift_jis(data)
    results["euc-kr"] = check_euc_kr(data)

    results["iso-8859-1"] = check_iso8859(data, "iso-8859-1")
    results["windows-1252"] = check_windows1252(data)
    results["iso-8859-2"] = check_iso8859(data, "iso-8859-2")
    results["iso-8859-5"] = check_iso8859(data, "iso-8859-5")
    results["iso-8859-7"] = check_iso8859(data, "iso-8859-7")
    results["iso-8859-9"] = check_iso8859(data, "iso-8859-9")

    results["cp866"] = check_cp866(data)
    results["cp1251"] = check_windows1251(data)
    results["koi8-r"] = check_koi8_r(data)

    if not results:
        return "utf-8", results

    best_encoding = max(results, key=results.get)  # type: ignore[arg-type]
    confidence = results[best_encoding]

    if confidence < 0.3:
        return "iso-8859-1", results

    return best_encoding, results


def check_utf8(data: bytes) -> float:
    """Check if data is valid UTF-8."""
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return 0.0

    has_multibyte = False
    i = 0
    while i < len(data):
        if data[i] < 0x80:
            i += 1
        elif data[i] & 0xE0 == 0xC0:
            if i + 1 >= len(data) or (data[i + 1] & 0xC0) != 0x80:
                return 0.0
            has_multibyte = True
            i += 2
        elif data[i] & 0xF0 == 0xE0:
            if (
                i + 2 >= len(data)
                or (data[i + 1] & 0xC0) != 0x80
                or (data[i + 2] & 0xC0) != 0x80
            ):
                return 0.0
            has_multibyte = True
            i += 3
        elif data[i] & 0xF8 == 0xF0:
            if (
                i + 3 >= len(data)
                or (data[i + 1] & 0xC0) != 0x80
                or (data[i + 2] & 0xC0) != 0x80
                or (data[i + 3] & 0xC0) != 0x80
            ):
                return 0.0
            has_multibyte = True
            i += 4
        else:
            return 0.0

    if has_multibyte:
        return 1.0
    return 0.9


def check_gb_series(data: bytes, encoding: str) -> float:
    """Check if data matches GB series encoding (GB2312/GBK)."""
    try:
        text = data.decode(encoding)
    except (UnicodeDecodeError, LookupError):
        return 0.0

    valid_cjk = 0
    has_ascii = False
    for char in text:
        if 0x4E00 <= ord(char) <= 0x9FFF:
            valid_cjk += 1
        elif 0x3400 <= ord(char) <= 0x4DBF:
            valid_cjk += 1
        elif char.isascii():
            has_ascii = True

    if valid_cjk == 0:
        return 0.0
    if has_ascii and valid_cjk < len(text) * 0.3:
        return 0.3
    return min(1.0, valid_cjk / (len(data) / 3))


def check_big5(data: bytes) -> float:
    """Check if data matches Big5 encoding."""
    try:
        text = data.decode("big5")
    except (UnicodeDecodeError, LookupError):
        return 0.0

    valid_cjk = 0
    has_ascii = False
    for char in text:
        if 0x4E00 <= ord(char) <= 0x9FFF:
            valid_cjk += 1
        elif 0xF900 <= ord(char) <= 0xFAFF:
            valid_cjk += 1
        elif char.isascii():
            has_ascii = True

    if valid_cjk == 0:
        return 0.0
    if has_ascii and valid_cjk < len(text) * 0.3:
        return 0.3
    return min(1.0, valid_cjk / (len(data) / 3))


def check_shift_jis(data: bytes) -> float:
    """Check if data matches Shift_JIS encoding."""
    try:
        text = data.decode("shift_jis")
    except (UnicodeDecodeError, LookupError):
        return 0.0

    valid_cjk = 0
    has_ascii = False
    for char in text:
        if 0x3040 <= ord(char) <= 0x309F:
            valid_cjk += 1
        elif 0x30A0 <= ord(char) <= 0x30FF:
            valid_cjk += 1
        elif 0x4E00 <= ord(char) <= 0x9FFF:
            valid_cjk += 1
        elif char.isascii():
            has_ascii = True

    if valid_cjk == 0:
        return 0.0
    if has_ascii and valid_cjk < len(text) * 0.3:
        return 0.3
    return min(1.0, valid_cjk / (len(data) / 3))


def check_euc_kr(data: bytes) -> float:
    """Check if data matches EUC-KR encoding."""
    try:
        text = data.decode("euc-kr")
    except (UnicodeDecodeError, LookupError):
        return 0.0

    valid_cjk = 0
    has_ascii = False
    for char in text:
        if 0xAC00 <= ord(char) <= 0xD7AF:
            valid_cjk += 1
        elif 0x4E00 <= ord(char) <= 0x9FFF:
            valid_cjk += 1
        elif char.isascii():
            has_ascii = True

    if valid_cjk == 0:
        return 0.0
    if has_ascii and valid_cjk < len(text) * 0.3:
        return 0.3
    return min(1.0, valid_cjk / (len(data) / 3))


def check_iso8859(data: bytes, encoding: str) -> float:
    """Check if data matches ISO-8859 series encoding."""
    try:
        text = data.decode(encoding)
    except (UnicodeDecodeError, LookupError):
        return 0.0

    valid_chars = 0
    for char in text:
        if char.isascii():
            continue
        if encoding == "iso-8859-1":
            valid_chars += 1
        elif encoding == "iso-8859-2":
            if 0x0100 <= ord(char) <= 0x017F or 0x0180 <= ord(char) <= 0x024F:
                valid_chars += 1
        elif encoding == "iso-8859-5":
            if 0x0400 <= ord(char) <= 0x04FF:
                valid_chars += 1
        elif encoding == "iso-8859-7":
            if 0x0370 <= ord(char) <= 0x03FF:
                valid_chars += 1
        elif encoding == "iso-8859-9":
            if 0x0100 <= ord(char) <= 0x017F:
                valid_chars += 1
    if valid_chars == 0:
        return 0.0
    return min(1.0, valid_chars / (len(data) / 2))


def check_windows1252(data: bytes) -> float:
    """Check if data matches Windows-1252 encoding."""
    try:
        text = data.decode("windows-1252")
    except UnicodeDecodeError:
        return 0.0

    valid_chars = 0
    for char in text:
        if char.isascii():
            continue
        if 0x0080 <= ord(char) <= 0x009F:
            valid_chars += 0.3
        elif 0x00A0 <= ord(char) <= 0x00FF:
            valid_chars += 1
    if valid_chars == 0:
        return 0.0
    return min(1.0, valid_chars / (len(data) / 2))


def check_windows1251(data: bytes) -> float:
    """Check if data matches Windows-1251 encoding."""
    try:
        text = data.decode("windows-1251")
    except UnicodeDecodeError:
        return 0.0

    valid_chars = 0
    for char in text:
        if char.isascii():
            continue
        if 0x0400 <= ord(char) <= 0x04FF:
            valid_chars += 1
    if valid_chars == 0:
        return 0.0
    return min(1.0, valid_chars / (len(data) / 2))


def check_cp866(data: bytes) -> float:
    """Check if data matches CP866 encoding."""
    try:
        text = data.decode("cp866")
    except UnicodeDecodeError:
        return 0.0

    valid_chars = 0
    for char in text:
        if char.isascii():
            continue
        if 0x0410 <= ord(char) <= 0x044F:
            valid_chars += 1
    if valid_chars == 0:
        return 0.0
    return min(1.0, valid_chars / (len(data) / 2))


def check_koi8_r(data: bytes) -> float:
    """Check if data matches KOI8-R encoding."""
    try:
        text = data.decode("koi8-r")
    except UnicodeDecodeError:
        return 0.0

    valid_chars = 0
    for char in text:
        if char.isascii():
            continue
        if 0x0410 <= ord(char) <= 0x043F:
            valid_chars += 1
    if valid_chars == 0:
        return 0.0
    return min(1.0, valid_chars / (len(data) / 2))


def convert_encoding(
    data: bytes, from_encoding: str, to_encoding: str = "utf-8"
) -> str:
    """Convert bytes from one encoding to another.

    Args:
        data: Input bytes
        from_encoding: Source encoding
        to_encoding: Target encoding (default: utf-8)

    Returns:
        Converted string
    """
    return data.decode(from_encoding).encode(to_encoding).decode(to_encoding)
