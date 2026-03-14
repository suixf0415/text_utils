"""Text cleaning utilities for whitespace and line handling."""

import re


def strip_whitespace(text: str) -> str:
    """Remove leading and trailing whitespace from text.

    Args:
        text: Input text to clean.

    Returns:
        Text with leading and trailing whitespace removed.
    """
    return text.strip()


def collapse_spaces(text: str) -> str:
    """Collapse multiple consecutive spaces into a single space.

    Args:
        text: Input text to clean.

    Returns:
        Text with multiple spaces replaced by single space.
    """
    return re.sub(r" +", " ", text)


def remove_newlines(text: str, replacement: str = " ") -> str:
    """Remove all newline characters from text.

    Args:
        text: Input text to clean.
        replacement: String to replace newlines with (default: single space).

    Returns:
        Text with newlines replaced.
    """
    return re.sub(r"[\n\r]+", replacement, text)


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
    return text.replace("\n", replacement).replace("\r", replacement)


def truncate_whitespace(text: str, max_consecutive: int = 1) -> str:
    """Limit consecutive whitespace to specified maximum.

    Args:
        text: Input text.
        max_consecutive: Maximum number of consecutive whitespace chars.

    Returns:
        Text with limited consecutive whitespace.
    """
    pattern = r" {%d,}" % (max_consecutive + 1)
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
