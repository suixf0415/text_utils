"""Language detection utilities for Chinese, English, Japanese, and Korean."""

from typing import Dict


LANG_ZH = "zh"
LANG_EN = "en"
LANG_JA = "ja"
LANG_KO = "ko"
LANG_UNKNOWN = "unknown"

ZH_RANGES = [
    (0x4E00, 0x9FFF),
    (0x3400, 0x4DBF),
    (0x20000, 0x2A6DF),
    (0x2A700, 0x2B73F),
    (0x2B740, 0x2B81F),
    (0x2B820, 0x2CEAF),
    (0x2CEB0, 0x2EBEF),
    (0x3000, 0x303F),
]

JA_HIRAGANA = (0x3040, 0x309F)
JA_KATAKANA = (0x30A0, 0x30FF)
JA_KANJI = [
    (0x4E00, 0x9FFF),
    (0x3400, 0x4DBF),
]

KO_HANGUL = (0xAC00, 0xD7AF)
KO_KANJI = [
    (0x4E00, 0x9FFF),
    (0x3400, 0x4DBF),
]

EN_ASCII_LA = (0x41, 0x5A)
EN_ASCII_LC = (0x61, 0x7A)


def _in_range(char: str, start: int, end: int) -> bool:
    code = ord(char)
    return start <= code <= end


def _in_ranges(char: str, ranges: list) -> bool:
    return any(_in_range(char, r[0], r[1]) for r in ranges)


def _count_chars(text: str) -> Dict[str, int]:
    counts = {
        "zh": 0,
        "ja_hira": 0,
        "ja_kata": 0,
        "ja_kanji": 0,
        "ko": 0,
        "ko_kanji": 0,
        "en": 0,
        "other": 0,
    }
    total = 0

    for char in text:
        if char.isspace() or char in ",.!?;:，。！？；：\n\r\t":
            continue

        total += 1

        if _in_range(char, *JA_HIRAGANA):
            counts["ja_hira"] += 1
        elif _in_range(char, *JA_KATAKANA):
            counts["ja_kata"] += 1
        elif _in_range(char, *KO_HANGUL):
            counts["ko"] += 1
        elif _in_ranges(char, ZH_RANGES):
            counts["zh"] += 1
        elif _in_ranges(char, JA_KANJI):
            counts["ja_kanji"] += 1
        elif _in_ranges(char, KO_KANJI):
            counts["ko_kanji"] += 1
        elif _in_range(char, *EN_ASCII_LA) or _in_range(char, *EN_ASCII_LC):
            counts["en"] += 1
        else:
            counts["other"] += 1

    return counts, total


def detect_language(text: str) -> str:
    """Detect language of the input text.

    Supports: Chinese (zh), English (en), Japanese (ja), Korean (ko).

    Args:
        text: Input text to detect language.

    Returns:
        Language code: 'zh', 'en', 'ja', 'ko', or 'unknown'.
    """
    if not text or not text.strip():
        return LANG_UNKNOWN

    counts, total = _count_chars(text)

    if total == 0:
        return LANG_UNKNOWN

    zh_ratio = counts["zh"] / total
    ja_hira_ratio = counts["ja_hira"] / total
    ja_kata_ratio = counts["ja_kata"] / total
    ja_kanji_ratio = counts["ja_kanji"] / total
    ko_ratio = counts["ko"] / total
    ko_kanji_ratio = counts["ko_kanji"] / total
    en_ratio = counts["en"] / total

    if ja_hira_ratio > 0.05 or ja_kata_ratio > 0.05:
        return LANG_JA

    if ko_ratio > 0.1:
        return LANG_KO

    if ko_kanji_ratio > 0.3 and ko_ratio < 0.1 and ja_kanji_ratio > 0.1:
        if zh_ratio > ko_kanji_ratio:
            return LANG_ZH
        return LANG_JA

    if zh_ratio > 0.15:
        return LANG_ZH

    if ja_kanji_ratio > 0.3 and zh_ratio < 0.1:
        return LANG_JA

    if en_ratio > 0.7:
        return LANG_EN

    if en_ratio > 0.3:
        if zh_ratio > 0.1:
            return LANG_ZH
        if ja_kanji_ratio > 0.1:
            return LANG_JA
        if ko_ratio > 0.1:
            return LANG_KO
        return LANG_EN

    if ja_kanji_ratio > 0.2 and zh_ratio < 0.1:
        return LANG_JA

    if zh_ratio > 0.1:
        return LANG_ZH

    if en_ratio > 0.1:
        return LANG_EN

    return LANG_UNKNOWN


def detect_language_detail(text: str) -> Dict[str, float]:
    """Detect language with confidence scores.

    Args:
        text: Input text to detect language.

    Returns:
        Dict with language codes as keys and confidence scores as values.
    """
    if not text or not text.strip():
        return {}

    counts, total = _count_chars(text)

    if total == 0:
        return {}

    scores: Dict[str, float] = {}

    zh_score = (
        counts["zh"] + counts["ja_kanji"] * 0.3 + counts["ko_kanji"] * 0.2
    ) / total
    ja_score = (
        counts["ja_hira"] + counts["ja_kata"] * 1.5 + counts["ja_kanji"] * 0.5
    ) / total
    ko_score = (counts["ko"] + counts["ko_kanji"] * 0.3) / total
    en_score = counts["en"] / total

    if zh_score > 0.05:
        scores[LANG_ZH] = round(zh_score, 3)
    if ja_score > 0.05:
        scores[LANG_JA] = round(ja_score, 3)
    if ko_score > 0.05:
        scores[LANG_KO] = round(ko_score, 3)
    if en_score > 0.05:
        scores[LANG_EN] = round(en_score, 3)

    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
