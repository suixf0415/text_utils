"""Line-based text processing utilities."""

import random
import re
from typing import List, Optional


def deduplicate(text: str, case_sensitive: bool = True) -> str:
    """Remove duplicate lines.

    Args:
        text: Input text with lines.
        case_sensitive: Whether to consider case when comparing lines.

    Returns:
        Text with duplicate lines removed.
    """
    lines = text.split("\n")
    if case_sensitive:
        seen = set()
        result = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                result.append(line)
    else:
        seen = set()
        result = []
        for line in lines:
            lower = line.lower()
            if lower not in seen:
                seen.add(lower)
                result.append(line)
    return "\n".join(result)


def sort_lines(text: str, reverse: bool = False, numeric: bool = False) -> str:
    """Sort lines alphabetically.

    Args:
        text: Input text with lines.
        reverse: Whether to sort in reverse order.
        numeric: Whether to sort numerically.

    Returns:
        Sorted lines.
    """
    lines = text.split("\n")
    if numeric:
        lines.sort(key=lambda x: int(x) if x.isdigit() else x, reverse=reverse)
    else:
        lines.sort(reverse=reverse)
    return "\n".join(lines)


def shuffle_lines(text: str) -> str:
    """Randomly shuffle lines.

    Args:
        text: Input text with lines.

    Returns:
        Shuffled lines.
    """
    lines = text.split("\n")
    random.shuffle(lines)
    return "\n".join(lines)


def reverse_lines(text: str) -> str:
    """Reverse the order of lines.

    Args:
        text: Input text with lines.

    Returns:
        Reversed lines.
    """
    lines = text.split("\n")
    lines.reverse()
    return "\n".join(lines)


def filter_lines(
    text: str, pattern: str, include: bool = True, ignore_case: bool = False
) -> str:
    """Filter lines by pattern.

    Args:
        text: Input text with lines.
        pattern: Regular expression pattern.
        include: Whether to include matching lines (True) or exclude them (False).
        ignore_case: Whether to ignore case when matching.

    Returns:
        Filtered lines.
    """
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    lines = text.split("\n")
    if include:
        result = [line for line in lines if regex.search(line)]
    else:
        result = [line for line in lines if not regex.search(line)]
    return "\n".join(result)


def filter_empty_lines(text: str) -> str:
    """Remove empty lines.

    Args:
        text: Input text with lines.

    Returns:
        Text with empty lines removed.
    """
    lines = text.split("\n")
    result = [line for line in lines if line.strip()]
    return "\n".join(result)


def number_lines(
    text: str, start: int = 1, width: int = 0, separator: str = ": "
) -> str:
    """Add line numbers.

    Args:
        text: Input text with lines.
        start: Starting line number.
        width: Minimum width for line numbers (0 = no padding).
        separator: String between number and line.

    Returns:
        Text with line numbers.
    """
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines, start=start):
        if width > 0:
            num = str(i).zfill(width)
        else:
            num = str(i)
        result.append(f"{num}{separator}{line}")
    return "\n".join(result)


def uniq_lines(text: str) -> str:
    """Remove consecutive duplicate lines (like Unix uniq).

    Args:
        text: Input text with lines.

    Returns:
        Text with consecutive duplicates removed.
    """
    lines = text.split("\n")
    result = []
    prev = None
    for line in lines:
        if line != prev:
            result.append(line)
            prev = line
    return "\n".join(result)


def head_lines(text: str, count: int = 10) -> str:
    """Get first N lines.

    Args:
        text: Input text with lines.
        count: Number of lines to return.

    Returns:
        First N lines.
    """
    lines = text.split("\n")
    return "\n".join(lines[:count])


def tail_lines(text: str, count: int = 10) -> str:
    """Get last N lines.

    Args:
        text: Input text with lines.
        count: Number of lines to return.

    Returns:
        Last N lines.
    """
    lines = text.split("\n")
    return "\n".join(lines[-count:])


def slice_lines(text: str, start: int = 0, end: Optional[int] = None) -> str:
    """Get lines by slice indices.

    Args:
        text: Input text with lines.
        start: Starting line index (0-based).
        end: Ending line index (exclusive), None for all remaining.

    Returns:
        Sliced lines.
    """
    lines = text.split("\n")
    return "\n".join(lines[start:end])


def join_lines(text: str, separator: str = " ") -> str:
    """Join lines with separator.

    Args:
        text: Input text with lines.
        separator: String to join lines with.

    Returns:
        Joined text.
    """
    lines = text.split("\n")
    return separator.join(lines)


def split_lines(text: str) -> List[str]:
    """Split text into lines.

    Args:
        text: Input text.

    Returns:
        List of lines.
    """
    return text.split("\n")


def count_lines(text: str, empty: bool = False) -> int:
    """Count lines in text.

    Args:
        text: Input text.
        empty: Whether to count empty lines only.

    Returns:
        Number of lines.
    """
    lines = text.split("\n")
    if empty:
        return sum(1 for line in lines if not line.strip())
    return len(lines)
