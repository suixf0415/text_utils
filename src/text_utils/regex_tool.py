"""Regular expression based text processing utilities."""

import re
from typing import List


def grep(
    pattern: str, text: str, ignore_case: bool = False, invert: bool = False
) -> List[str]:
    """Search for lines matching a pattern.

    Args:
        pattern: Regular expression pattern.
        text: Input text to search.
        ignore_case: Whether to ignore case.
        invert: Whether to return non-matching lines instead.

    Returns:
        List of matching lines.
    """
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    lines = text.split("\n")
    if invert:
        return [line for line in lines if not regex.search(line)]
    return [line for line in lines if regex.search(line)]


def grep_with_context(
    pattern: str,
    text: str,
    ignore_case: bool = False,
    before: int = 0,
    after: int = 0,
) -> List[str]:
    """Search for lines matching a pattern with context.

    Args:
        pattern: Regular expression pattern.
        text: Input text to search.
        ignore_case: Whether to ignore case.
        before: Number of lines to include before match.
        after: Number of lines to include after match.

    Returns:
        List of matching lines with context.
    """
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines):
        if regex.search(line):
            start = max(0, i - before)
            end = min(len(lines), i + after + 1)
            for j in range(start, end):
                result.append(lines[j])
    return result


def replace(
    pattern: str,
    text: str,
    replacement: str = "",
    count: int = 0,
    ignore_case: bool = False,
) -> str:
    """Replace pattern with replacement string.

    Args:
        pattern: Regular expression pattern.
        text: Input text.
        replacement: Replacement string.
        count: Maximum replacements (0 = all).
        ignore_case: Whether to ignore case.

    Returns:
        Text with replacements made.
    """
    flags = re.IGNORECASE if ignore_case else 0
    if count > 0:
        return re.sub(pattern, replacement, text, count=count, flags=flags)
    return re.sub(pattern, replacement, text, flags=flags)


def replace_callback(
    pattern: str,
    text: str,
    callback,
    ignore_case: bool = False,
) -> str:
    """Replace pattern using a callback function.

    Args:
        pattern: Regular expression pattern.
        text: Input text.
        callback: Function that takes match object and returns replacement string.
        ignore_case: Whether to ignore case.

    Returns:
        Text with replacements made.
    """
    flags = re.IGNORECASE if ignore_case else 0
    return re.sub(pattern, callback, text, flags=flags)


def extract(
    pattern: str, text: str, group: int = 0, ignore_case: bool = False
) -> List[str]:
    """Extract matches from text.

    Args:
        pattern: Regular expression pattern.
        text: Input text.
        group: Capture group number to extract (0 = full match).
        ignore_case: Whether to ignore case.

    Returns:
        List of extracted matches.
    """
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    matches = regex.findall(text)
    if group == 0:
        return matches
    return [m[group - 1] if isinstance(m, tuple) else m for m in matches]


def extract_groups(pattern: str, text: str, ignore_case: bool = False) -> List[tuple]:
    """Extract all capture groups from matches.

    Args:
        pattern: Regular expression pattern.
        text: Input text.
        ignore_case: Whether to ignore case.

    Returns:
        List of tuples containing capture groups.
    """
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    return regex.findall(text)


def split_by_pattern(pattern: str, text: str) -> List[str]:
    """Split text by pattern.

    Args:
        pattern: Regular expression pattern.
        text: Input text.

    Returns:
        List of text segments.
    """
    return re.split(pattern, text)


def find_all(pattern: str, text: str, ignore_case: bool = False) -> List[dict]:
    """Find all matches with positions.

    Args:
        pattern: Regular expression pattern.
        text: Input text.
        ignore_case: Whether to ignore case.

    Returns:
        List of dicts with match info (text, start, end).
    """
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    result = []
    for match in regex.finditer(text):
        result.append(
            {
                "text": match.group(),
                "start": match.start(),
                "end": match.end(),
            }
        )
    return result


def count_matches(pattern: str, text: str, ignore_case: bool = False) -> int:
    """Count number of matches.

    Args:
        pattern: Regular expression pattern.
        text: Input text.
        ignore_case: Whether to ignore case.

    Returns:
        Number of matches found.
    """
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    return len(regex.findall(text))


def is_match(pattern: str, text: str, ignore_case: bool = False) -> bool:
    """Check if pattern matches anywhere in text.

    Args:
        pattern: Regular expression pattern.
        text: Input text.
        ignore_case: Whether to ignore case.

    Returns:
        True if pattern matches.
    """
    flags = re.IGNORECASE if ignore_case else 0
    return bool(re.search(pattern, text, flags))


def full_match(pattern: str, text: str, ignore_case: bool = False) -> bool:
    """Check if pattern fully matches the text.

    Args:
        pattern: Regular expression pattern.
        text: Input text.
        ignore_case: Whether to ignore case.

    Returns:
        True if pattern fully matches.
    """
    flags = re.IGNORECASE if ignore_case else 0
    return bool(re.fullmatch(pattern, text, flags))
