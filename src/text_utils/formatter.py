"""Text formatting utilities for case conversion and naming styles."""

import re
from typing import List


def to_upper(text: str) -> str:
    """Convert text to uppercase.

    Args:
        text: Input text.

    Returns:
        Uppercase text.
    """
    return text.upper()


def to_lower(text: str) -> str:
    """Convert text to lowercase.

    Args:
        text: Input text.

    Returns:
        Lowercase text.
    """
    return text.lower()


def to_title(text: str) -> str:
    """Convert text to title case.

    Args:
        text: Input text.

    Returns:
        Title cased text.
    """
    return text.title()


def to_sentence(text: str) -> str:
    """Convert text to sentence case.

    Args:
        text: Input text.

    Returns:
        Sentence cased text.
    """
    return text.capitalize()


def to_camel_case(text: str) -> str:
    """Convert text to camelCase.

    Args:
        text: Input text (typically snake_case or space-separated).

    Returns:
        camelCase formatted text.
    """
    words = _split_into_words(text)
    if not words:
        return ""
    first = words[0].lower()
    rest = [w.capitalize() for w in words[1:]]
    return first + "".join(rest)


def to_pascal_case(text: str) -> str:
    """Convert text to PascalCase (aka UpperCamelCase).

    Args:
        text: Input text.

    Returns:
        PascalCase formatted text.
    """
    words = _split_into_words(text)
    return "".join(w.capitalize() for w in words)


def to_snake_case(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Input text.

    Returns:
        snake_case formatted text.
    """
    words = _split_into_words(text)
    return "_".join(w.lower() for w in words)


def to_kebab_case(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Input text.

    Returns:
        kebab-case formatted text.
    """
    words = _split_into_words(text)
    return "-".join(w.lower() for w in words)


def to_constant_case(text: str) -> str:
    """Convert text to CONSTANT_CASE (upper snake case).

    Args:
        text: Input text.

    Returns:
        CONSTANT_CASE formatted text.
    """
    return to_snake_case(text).upper()


def to_dot_case(text: str) -> str:
    """Convert text to dot.case.

    Args:
        text: Input text.

    Returns:
        dot.case formatted text.
    """
    words = _split_into_words(text)
    return ".".join(w.lower() for w in words)


def _split_into_words(text: str) -> List[str]:
    """Split text into words using various separators.

    Args:
        text: Input text.

    Returns:
        List of words.
    """
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"[-_\s]+", " ", text)
    words = text.split()
    return [w for w in words if w]


def invert_case(text: str) -> str:
    """Invert the case of each character.

    Args:
        text: Input text.

    Returns:
        Text with inverted case.
    """
    return text.swapcase()


def capitalize_words(text: str, exceptions: List[str] = None) -> str:  # type: ignore[assignment]
    """Capitalize each word, with optional exceptions.

    Args:
        text: Input text.
        exceptions: Words to not capitalize (e.g., ['and', 'or', 'the']).

    Returns:
        Text with each word capitalized.
    """
    if exceptions is None:
        exceptions = []
    exceptions_set = set(e.lower() for e in exceptions)
    words = text.split()
    result = []
    for word in words:
        if word.lower() in exceptions_set:
            result.append(word.lower())
        else:
            result.append(word.capitalize())
    return " ".join(result)
