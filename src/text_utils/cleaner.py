"""Text cleaning utilities for whitespace and line handling."""

import re

CJK_SPACE = "\u3000"
NBSP = "\u00a0"
WHITESPACE_CHARS = r" [\t\u3000\u00A0]"


def strip_whitespace(text: str) -> str:
    """Remove leading and trailing whitespace from text.

    Args:
        text: Input text to clean.

    Returns:
        Text with leading and trailing whitespace removed.
    """
    return text.strip()


def collapse_spaces(text: str, include_tabs: bool = False) -> str:
    """Collapse multiple consecutive spaces into a single space.

    Args:
        text: Input text to clean.
        include_tabs: Whether to also collapse tabs (default: False).

    Returns:
        Text with multiple spaces replaced by single space.
    """
    if include_tabs:
        return re.sub(r"[ \t\u3000\u00A0]+", " ", text)
    return re.sub(r"[ \u3000\u00A0]+", " ", text)


def remove_newlines(text: str, replacement: str = " ") -> str:
    """Remove all newline characters from text.

    Args:
        text: Input text to clean.
        replacement: String to replace newlines with (default: single space).

    Returns:
        Text with newlines replaced.
    """
    return re.sub(r"[\n\r\v\f\u0085\u2028\u2029]+", replacement, text)


def normalize_whitespace(text: str) -> str:
    """Normalize all whitespace to single spaces and trim edges.

    This is a combination of strip_whitespace, collapse_spaces,
    and remove_newlines.

    Args:
        text: Input text to normalize.

    Returns:
        Fully normalized text with consistent whitespace.
    """
    text = remove_newlines(text, " ")
    text = collapse_spaces(text)
    return text.strip()


def remove_empty_lines(text: str) -> str:
    """Remove empty lines from multi-line text.

    Args:
        text: Input text with potential empty lines.

    Returns:
        Text with empty lines removed.
    """
    lines = text.split("\n")
    non_empty = [line for line in lines if line.strip()]
    return "\n".join(non_empty)


def strip_lines(text: str) -> str:
    """Strip whitespace from the beginning and end of each line.

    Args:
        text: Input multi-line text.

    Returns:
        Text with each line trimmed.
    """
    lines = text.split("\n")
    stripped = [line.strip() for line in lines]
    return "\n".join(stripped)


def remove_line_breaks(text: str, replacement: str = " ") -> str:
    """Remove all line breaks, keeping content on single line.

    Args:
        text: Input text.
        replacement: String to replace line breaks with.

    Returns:
        Text with line breaks replaced.
    """
    return (
        text.replace("\r\n", replacement)
        .replace("\r", replacement)
        .replace("\n", replacement)
    )


def remove_invisible_chars(text: str) -> str:
    """Remove invisible/zero-width characters from text.

    Removes zero-width space (\\u200B), zero-width joiner (\\u200D),
    zero-width non-joiner (\\u200C), left-to-right mark (\\u200E),
    right-to-left mark (\\u200F), and other invisible characters.

    Args:
        text: Input text.

    Returns:
        Text with invisible characters removed.
    """
    invisible_chars = [
        "\u00ad",
        "\u200b",
        "\u200c",
        "\u200d",
        "\u200e",
        "\u200f",
        "\ufeff",
    ]
    for char in invisible_chars:
        text = text.replace(char, "")
    return text


def truncate_whitespace(text: str, max_consecutive: int = 1) -> str:
    """Limit consecutive whitespace to specified maximum.

    Args:
        text: Input text.
        max_consecutive: Maximum number of consecutive whitespace chars.

    Returns:
        Text with limited consecutive whitespace.
    """
    if max_consecutive < 0:
        raise ValueError("max_consecutive must be non-negative")
    if max_consecutive == 0:
        return re.sub(r"[ \t\u3000\u00A0\n\r]+", "", text)
    pattern = r"[ \t\u3000\u00A0]{%d,}" % (max_consecutive + 1)
    return re.sub(pattern, " " * max_consecutive, text)


def clean_text(
    text: str, strip: bool = True, collapse: bool = True, rm_newlines: bool = False
) -> str:
    """Clean text with configurable options.

    Args:
        text: Input text to clean.
        strip: Whether to strip leading/trailing whitespace.
        collapse: Whether to collapse multiple spaces.
        rm_newlines: Whether to remove newline characters.

    Returns:
        Cleaned text.
    """
    if strip:
        text = text.strip()
    if collapse:
        text = collapse_spaces(text)
    if rm_newlines:
        text = remove_newlines(text, " ")
    return text
