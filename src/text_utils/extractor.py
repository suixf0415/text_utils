"""Text extraction utilities for common patterns like emails, phones, URLs, etc."""

import re
from ipaddress import ip_address, IPv6Address
from typing import List

EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

PHONE_CN_PATTERN = r"(?:\+\d{1,3}[\s\-]*)?(?:1[3-9]\d(?:[\-\s]?\d{4}){2}|(?:400|800)[\-\s]?\d{3,4}[\-\s]?\d{4}|0[1-9]\d{0,2}[\-\s]?\d{7,8})"

PHONE_US_PATTERN = r"(?:\+1)?(?:\([0-9]{3}\)|[0-9]{3})[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}"

URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'

IPV4_PATTERN = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"

IPV6_PATTERN = r"(?:[0-9a-fA-F]{1,4}:|:|::)[0-9a-fA-F:.]*(?:%[0-9a-zA-Z]+)?"

ID_CARD_CN_PATTERN = (
    r"[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]"
)

HASHTAG_PATTERN = r"#[a-zA-Z0-9_]+"

MENTION_PATTERN = r"@[a-zA-Z0-9_]+"

DATE_ISO_PATTERN = r"\d{4}-\d{2}-\d{2}"

DATE_CN_PATTERN = r"\d{4}年\d{1,2}月\d{1,2}日"


def extract_emails(text: str, deduplicate: bool = True) -> List[str]:
    """Extract email addresses from text.

    Args:
        text: Input text.
        deduplicate: Whether to remove duplicates.

    Returns:
        List of email addresses.
    """
    emails = re.findall(EMAIL_PATTERN, text)
    if deduplicate:
        return list(dict.fromkeys(emails))
    return emails


def extract_phones(
    text: str, region: str = "cn", deduplicate: bool = True
) -> List[str]:
    """Extract phone numbers from text.

    Args:
        text: Input text.
        region: Phone region ('cn' for China, 'us' for US).
        deduplicate: Whether to remove duplicates.

    Returns:
        List of phone numbers.
    """
    if region == "cn":
        pattern = PHONE_CN_PATTERN
    elif region == "us":
        pattern = PHONE_US_PATTERN
    else:
        pattern = PHONE_CN_PATTERN

    phones = re.findall(pattern, text)
    if deduplicate:
        return list(dict.fromkeys(phones))
    return phones


def extract_urls(text: str, deduplicate: bool = True) -> List[str]:
    """Extract URLs from text.

    Args:
        text: Input text.
        deduplicate: Whether to remove duplicates.

    Returns:
        List of URLs.
    """
    urls = re.findall(URL_PATTERN, text)
    if deduplicate:
        return list(dict.fromkeys(urls))
    return urls


def extract_ipv4(text: str, deduplicate: bool = True) -> List[str]:
    """Extract IPv4 addresses from text.

    Args:
        text: Input text.
        deduplicate: Whether to remove duplicates.

    Returns:
        List of IPv4 addresses.
    """
    ips = re.findall(IPV4_PATTERN, text)
    if deduplicate:
        return list(dict.fromkeys(ips))
    return ips


def extract_ipv6(text: str, deduplicate: bool = True) -> List[str]:
    """Extract IPv6 addresses from text.

    Args:
        text: Input text.
        deduplicate: Whether to remove duplicates.

    Returns:
        List of IPv6 addresses.
    """
    candidates = re.findall(IPV6_PATTERN, text, re.IGNORECASE)
    ips = []
    for cand in candidates:
        if len(cand) < 2:
            continue
        addr_part = cand.split("%")[0] if "%" in cand else cand
        try:
            addr = ip_address(addr_part)
            if isinstance(addr, IPv6Address):
                ips.append(cand)
        except ValueError:
            pass
    if deduplicate:
        return list(dict.fromkeys(ips))
    return ips


def extract_id_cards(text: str, deduplicate: bool = True) -> List[str]:
    """Extract Chinese ID card numbers from text.

    Args:
        text: Input text.
        deduplicate: Whether to remove duplicates.

    Returns:
        List of ID card numbers.
    """
    ids = re.findall(ID_CARD_CN_PATTERN, text)
    if deduplicate:
        return list(dict.fromkeys(ids))
    return ids


def extract_hashtags(text: str, deduplicate: bool = True) -> List[str]:
    """Extract hashtags from text.

    Args:
        text: Input text.
        deduplicate: Whether to remove duplicates.

    Returns:
        List of hashtags.
    """
    tags = re.findall(HASHTAG_PATTERN, text)
    if deduplicate:
        return list(dict.fromkeys(tags))
    return tags


def extract_mentions(text: str, deduplicate: bool = True) -> List[str]:
    """Extract @mentions from text.

    Args:
        text: Input text.
        deduplicate: Whether to remove duplicates.

    Returns:
        List of mentions.
    """
    mentions = re.findall(MENTION_PATTERN, text)
    if deduplicate:
        return list(dict.fromkeys(mentions))
    return mentions


def extract_dates(
    text: str, format: str = "iso", deduplicate: bool = True
) -> List[str]:
    """Extract dates from text.

    Args:
        text: Input text.
        format: Date format ('iso' or 'cn').
        deduplicate: Whether to remove duplicates.

    Returns:
        List of dates.
    """
    if format == "iso":
        pattern = DATE_ISO_PATTERN
    elif format == "cn":
        pattern = DATE_CN_PATTERN
    else:
        pattern = DATE_ISO_PATTERN

    dates = re.findall(pattern, text)
    if deduplicate:
        return list(dict.fromkeys(dates))
    return dates


def extract_numbers(
    text: str, decimal: bool = True, deduplicate: bool = True
) -> List[str]:
    """Extract numbers from text.

    Args:
        text: Input text.
        decimal: Whether to include decimal numbers.
        deduplicate: Whether to remove duplicates.

    Returns:
        List of numbers as strings.
    """
    if decimal:
        pattern = r"-?\d+\.?\d*"
    else:
        pattern = r"-?\d+"

    numbers = re.findall(pattern, text)
    if deduplicate:
        return list(dict.fromkeys(numbers))
    return numbers


def extract_words(
    text: str, min_length: int = 1, deduplicate: bool = True
) -> List[str]:
    """Extract words from text.

    Args:
        text: Input text.
        min_length: Minimum word length.
        deduplicate: Whether to remove duplicates.

    Returns:
        List of words.
    """
    words = re.findall(r"[a-zA-Z]+", text)
    words = [w for w in words if len(w) >= min_length]
    if deduplicate:
        return list(dict.fromkeys(words))
    return words


def extract_hex_colors(text: str, deduplicate: bool = True) -> List[str]:
    """Extract hexadecimal color codes from text.

    Args:
        text: Input text.
        deduplicate: Whether to remove duplicates.

    Returns:
        List of hex color codes.
    """
    colors = re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", text)
    if deduplicate:
        return list(dict.fromkeys(colors))
    return colors
