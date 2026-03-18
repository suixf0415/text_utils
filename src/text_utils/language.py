"""Language detection utilities."""

from typing import Dict, Tuple

LANG_EN = "en"
LANG_FR = "fr"
LANG_DE = "de"
LANG_ES = "es"
LANG_IT = "it"
LANG_PT = "pt"
LANG_NL = "nl"
LANG_ZH = "zh"
LANG_JA = "ja"
LANG_KO = "ko"
LANG_MN = "mn"
LANG_UNKNOWN = "unknown"

_LATIN_LANG = {LANG_EN, LANG_FR, LANG_DE, LANG_ES, LANG_IT, LANG_PT, LANG_NL}

_LATIN_SPECIAL_CHARS: Dict[str, Tuple[str, ...]] = {
    LANG_FR: ("é", "è", "ê", "ë", "ç", "œ", "à", "û", "ù", "ô", "î", "ï"),
    LANG_DE: ("ä", "ö", "ü", "ß", "Ä", "Ö", "Ü"),
    LANG_ES: ("ñ", "á", "é", "í", "ó", "ú", "ü", "¿", "¡"),
    LANG_IT: ("é", "è", "à", "ò", "ù", "ì", "î"),
    LANG_PT: ("ç", "ã", "õ", "á", "é", "í", "ó", "ú"),
    LANG_NL: ("ij", "ö", "ë", "ï"),
}

_LATIN_KEYWORDS: Dict[str, Tuple[str, ...]] = {
    LANG_EN: (
        "the",
        "is",
        "are",
        "was",
        "were",
        "be",
        "have",
        "has",
        "and",
        "or",
        "but",
        "that",
        "this",
        "which",
        "with",
        "from",
        "they",
        "been",
        "will",
        "would",
        "could",
        "should",
        "their",
        "there",
        "where",
        "when",
        "what",
        "who",
        "how",
        "not",
        "all",
        "also",
        "into",
        "than",
        "other",
        "some",
        "them",
        "then",
        "time",
        "only",
        "very",
        "just",
        "can",
        "may",
        "any",
        "such",
        "more",
        "most",
        "new",
        "one",
        "two",
        "our",
        "out",
        "day",
        "get",
        "now",
        "see",
        "way",
        "made",
        "like",
        "make",
        "know",
        "take",
        "come",
        "here",
        "want",
        "use",
        "find",
        "give",
        "tell",
        "try",
        "call",
        "look",
        "think",
        "back",
        "even",
        "need",
        "feel",
        "say",
        "said",
    ),
    LANG_FR: (
        "les",
        "une",
        "des",
        "sont",
        "être",
        "avoir",
        "dans",
        "pour",
        "plus",
        "par",
        "avec",
        "cette",
        "ces",
        "nous",
        "vous",
        "elles",
        "mon",
        "ton",
        "son",
        "mes",
        "tes",
        "ses",
        "notre",
        "votre",
        "leur",
        "comme",
        "fait",
        "bien",
        "peut",
        "sans",
        "mais",
        "très",
        "leur",
        "dont",
        "encore",
        "cela",
        "donc",
        "sous",
        "chez",
        "faire",
        "alors",
        "cette",
        "après",
        "avant",
        "autres",
        "entre",
        "moins",
        "autour",
        "toute",
        "toutes",
        "rien",
        "autre",
        "mieux",
        "chaque",
        "certains",
        "personne",
        "toujours",
        "souvent",
        "jamais",
        "première",
        "deuxième",
    ),
    LANG_DE: (
        "der",
        "die",
        "das",
        "und",
        "ist",
        "sind",
        "war",
        "waren",
        "sein",
        "haben",
        "hat",
        "werden",
        "wird",
        "kann",
        "können",
        "nicht",
        "eine",
        "einer",
        "einem",
        "einen",
        "sich",
        "dass",
        "dieser",
        "diese",
        "dieses",
        "nach",
        "aus",
        "bei",
        "über",
        "durch",
        "ohne",
        "gegen",
        "vom",
        "zum",
        "zur",
        "wurde",
        "wurden",
        "habe",
        "hast",
        "habt",
        "seid",
        "wird",
        "wirst",
        "werden",
        "seine",
        "ihre",
        "unsere",
        "euren",
        "deren",
        "dessen",
        "welche",
        "welcher",
        "welches",
        "alle",
        "allem",
        "allen",
        "aller",
        "alles",
        "etwas",
        "nichts",
        "viel",
        "wenig",
        "mehr",
        "alle",
        "andere",
    ),
    LANG_ES: (
        "los",
        "las",
        "unos",
        "unas",
        "son",
        "estar",
        "ser",
        "haber",
        "tener",
        "desde",
        "entre",
        "hasta",
        "sobre",
        "donde",
        "cuando",
        "como",
        "hacer",
        "puede",
        "tiene",
        "tienen",
        "ser",
        "estar",
        "había",
        "hubo",
        "hace",
        "hizo",
        "esto",
        "ese",
        "esta",
        "esa",
        "estos",
        "esas",
        "todos",
        "todas",
        "cada",
        "mucho",
        "poco",
        "muy",
        "tan",
        "más",
        "menos",
        "mismo",
        "misma",
        "otros",
        "otras",
        "algunos",
        "algunas",
        "cual",
        "cuales",
        "quien",
        "quieren",
        "nada",
        "nadie",
        "cada",
        "solo",
        "sólo",
        "aunque",
        "porque",
        "mientras",
        "antes",
        "después",
        "siempre",
        "nunca",
        "tarde",
        "pronto",
        "bien",
        "mal",
        "mucha",
        "muchas",
        "poca",
        "pocas",
        "grande",
        "grandes",
        "pequeño",
        "pequeña",
        "nuevo",
        "nueva",
        "viejo",
        "vieja",
        "primero",
        "segundo",
        "tercero",
    ),
    LANG_IT: (
        "gli",
        "uno",
        "una",
        "sono",
        "essere",
        "avere",
        "che",
        "chi",
        "questo",
        "questa",
        "quello",
        "quella",
        "altro",
        "altera",
        "altri",
        "alle",
        "anche",
        "ancora",
        "dove",
        "quando",
        "come",
        "fare",
        "così",
        "proprio",
        "dopo",
        "prima",
        "sempre",
        "mai",
        "molto",
        "poco",
        "troppo",
        "tanto",
        "tutta",
        "tutte",
        "tutti",
        "nessuno",
        "qualcosa",
        "qualcuno",
        "ogni",
        "ognuno",
        "altro",
        "stesso",
        "stessa",
        "nuovo",
        "nuova",
        "buono",
        "buona",
        "grande",
        "piccolo",
        "piccola",
        "primo",
        "prima",
        "secondo",
        "oggi",
        "ieri",
        "domani",
        "ora",
        "mai",
        "più",
        "meno",
        "così",
        "bene",
        "male",
        "meglio",
        "peggio",
        "potere",
        "dovere",
        "volere",
        "voglia",
        "fare",
        "dire",
        "vedere",
        "sapere",
        "conoscere",
        "parlare",
        "sentire",
        "trovare",
        "dare",
        "prendere",
        "lavorare",
        "vivere",
        "morire",
        "nascere",
        "credere",
        "pensare",
        "amare",
        "odiare",
        "sperare",
        "temere",
        "dimenticare",
        "ricordare",
        "capire",
        "leggere",
        "scrivere",
        "ascoltare",
        "guardare",
    ),
    LANG_PT: (
        "são",
        "estar",
        "ter",
        "haver",
        "quando",
        "como",
        "está",
        "está",
        "for",
        "forem",
        "ser",
        "fora",
        "fazer",
        "pode",
        "podem",
        "tem",
        "têm",
        "era",
        "foram",
        "foi",
        "fiz",
        "fez",
        "isso",
        "esse",
        "esta",
        "essa",
        "estes",
        "estas",
        "esses",
        "aquilo",
        "todo",
        "toda",
        "todos",
        "todas",
        "cada",
        "muito",
        "pouco",
        "muita",
        "pouca",
        "tantas",
        "tantos",
        "quais",
        "quem",
        "qual",
        "nada",
        "ninguém",
        "alguém",
        "todos",
        "nenhum",
        "algum",
        "alguma",
        "alguns",
        "algumas",
        "outro",
        "outra",
        "outros",
        "outras",
        "próprio",
        "própria",
        "melho",
        "pior",
        "maior",
        "menor",
        "melhor",
        "pior",
        "grande",
        "pequeno",
        "nova",
        "velho",
        "velha",
        "primeiro",
        "segundo",
        "último",
        "cada",
        "porque",
        "embora",
        "enquanto",
        "depois",
        "antes",
        "sempre",
        "nunca",
        "jamais",
        "já",
        "ainda",
        "agora",
        "aqui",
        "ali",
        "lá",
        "perto",
        "longe",
        "dentro",
        "fora",
        "em",
        "com",
        "sem",
        "para",
        "por",
        "sobre",
        "entre",
        "através",
        "desde",
        "até",
        "contra",
        "sob",
    ),
    LANG_NL: (
        "het",
        "zijn",
        "waren",
        "worden",
        "wordt",
        "kunnen",
        "moeten",
        "zal",
        "zullen",
        "niet",
        "van",
        "dat",
        "dit",
        "die",
        "wat",
        "wie",
        "waar",
        "hoe",
        "wanneer",
        "omdat",
        "dus",
        "maar",
        "toch",
        "ook",
        "al",
        "nog",
        "weer",
        "alleen",
        "zelfs",
        "veel",
        "weinig",
        "alle",
        "ander",
        "andere",
        "elk",
        "ieder",
        "iets",
        "iemand",
        "niemand",
        "iedereen",
        "niets",
        "alles",
        "meer",
        "minder",
        "meeste",
        "minste",
        "groot",
        "grote",
        "klein",
        "kleine",
        "nieuw",
        "nieuwe",
        "oud",
        "oude",
        "goed",
        "goede",
        "slecht",
        "slechte",
        "mooi",
        "mooie",
        "lelijk",
        "jij",
        "je",
        "u",
        "wij",
        "we",
        "jullie",
        "hen",
        "zij",
        "hem",
        "haar",
        "mijn",
        "jouw",
        "ons",
        "onze",
        "uw",
        "hun",
        "deze",
        "wie",
        "wat",
        "welk",
        "welke",
        "waarom",
        "allemaal",
        "allebei",
        "beide",
        "beiden",
    ),
}

_HIRAGANA_RANGE = (0x3040, 0x309F)
_KATAKANA_RANGE = (0x30A0, 0x30FF)

_CHINESE_RANGES = (
    (0x4E00, 0x9FFF),
    (0x3400, 0x4DBF),
    (0x20000, 0x2A6DF),
    (0x2A700, 0x2B73F),
    (0x2B740, 0x2B81F),
    (0x2B820, 0x2CEAF),
    (0x2CEB0, 0x2EBEF),
)

_KOREAN_RANGES = (
    (0xAC00, 0xD7AF),
    (0x1100, 0x11FF),
    (0x3130, 0x318F),
    (0xA960, 0xA97F),
    (0xD7B0, 0xD7FF),
)

_MONGOLIAN_RANGES = ((0x1800, 0x18AF),)


def _count_chars_in_ranges(text: str, ranges: Tuple[Tuple[int, int], ...]) -> int:
    count = 0
    for char in text:
        code = ord(char)
        for start, end in ranges:
            if start <= code <= end:
                count += 1
                break
    return count


def _count_special_chars(text: str, special_chars: Tuple[str, ...]) -> int:
    return sum(text.count(char) for char in special_chars)


def _count_keywords(text: str, keywords: Tuple[str, ...]) -> int:
    text_lower = text.lower()
    count = 0
    for keyword in keywords:
        count += text_lower.count(keyword)
    return count


def _has_only_punctuation_and_spaces(text: str) -> bool:
    for char in text:
        if char.isalnum():
            return False
    return True


def _count_alpha_chars(text: str) -> int:
    return sum(1 for char in text if char.isalpha())


def detect_language(text: str) -> str:
    """Detect the language of the given text.

    Args:
        text: Input text to detect language for

    Returns:
        Language code (e.g., 'en', 'fr', 'zh', 'ja', 'ko', 'mn')
    """
    if not text or text.isspace():
        return LANG_UNKNOWN

    clean_text = text.strip()
    if not clean_text:
        return LANG_UNKNOWN

    if _has_only_punctuation_and_spaces(clean_text):
        return LANG_UNKNOWN

    mongolian_count = _count_chars_in_ranges(clean_text, _MONGOLIAN_RANGES)
    total_chars = len(clean_text.replace(" ", "").replace("\n", ""))

    if total_chars == 0:
        return LANG_UNKNOWN

    if mongolian_count / total_chars > 0.2:
        return LANG_MN

    hiragana_count = _count_chars_in_ranges(clean_text, (_HIRAGANA_RANGE,))
    katakana_count = _count_chars_in_ranges(clean_text, (_KATAKANA_RANGE,))
    japanese_script_count = hiragana_count + katakana_count
    chinese_count = _count_chars_in_ranges(clean_text, _CHINESE_RANGES)

    if japanese_script_count > 0:
        if japanese_script_count / total_chars > 0.1:
            return LANG_JA
    if chinese_count / total_chars > 0.3 and japanese_script_count == 0:
        return LANG_ZH

    korean_count = _count_chars_in_ranges(clean_text, _KOREAN_RANGES)
    if korean_count / total_chars > 0.3:
        return LANG_KO

    alpha_count = _count_alpha_chars(clean_text)
    if alpha_count == 0:
        return LANG_UNKNOWN

    latin_count = _count_chars_in_ranges(clean_text, ((0x0000, 0x024F),))
    if latin_count / alpha_count < 0.7:
        return LANG_UNKNOWN

    scores: Dict[str, float] = {}
    for lang in _LATIN_LANG:
        score = 0.0

        special_chars = _LATIN_SPECIAL_CHARS.get(lang, ())
        if special_chars:
            special_count = _count_special_chars(clean_text, special_chars)
            score += special_count * 10.0

        keywords = _LATIN_KEYWORDS.get(lang, ())
        if keywords:
            keyword_count = _count_keywords(clean_text, keywords)
            score += keyword_count * 1.0

        if score > 0:
            scores[lang] = score

    if not scores or max(scores.values()) < 3:
        return LANG_EN

    return max(scores, key=scores.get)


def detect_language_detail(text: str) -> Dict[str, float]:
    """Detect language with confidence scores for each language.

    Args:
        text: Input text to detect language for

    Returns:
        Dictionary mapping language codes to confidence scores (0-1)
    """
    if not text or text.isspace():
        return {}

    clean_text = text.strip()
    if not clean_text:
        return {}

    if _has_only_punctuation_and_spaces(clean_text):
        return {}

    result: Dict[str, float] = {}

    mongolian_count = _count_chars_in_ranges(clean_text, _MONGOLIAN_RANGES)
    total_chars = len(clean_text.replace(" ", "").replace("\n", ""))

    if total_chars == 0:
        return {}

    if mongolian_count > 0:
        result[LANG_MN] = min(mongolian_count / total_chars, 1.0)

    hiragana_count = _count_chars_in_ranges(clean_text, (_HIRAGANA_RANGE,))
    katakana_count = _count_chars_in_ranges(clean_text, (_KATAKANA_RANGE,))
    japanese_script_count = hiragana_count + katakana_count
    chinese_count = _count_chars_in_ranges(clean_text, _CHINESE_RANGES)

    if japanese_script_count > 0:
        result[LANG_JA] = min(japanese_script_count / total_chars, 1.0)

    if chinese_count > 0:
        result[LANG_ZH] = min(chinese_count / total_chars, 1.0)

    korean_count = _count_chars_in_ranges(clean_text, _KOREAN_RANGES)
    if korean_count > 0:
        result[LANG_KO] = min(korean_count / total_chars, 1.0)

    alpha_count = _count_alpha_chars(clean_text)
    if alpha_count > 0:
        latin_count = _count_chars_in_ranges(clean_text, ((0x0000, 0x024F),))
        if latin_count / alpha_count >= 0.7:
            scores: Dict[str, float] = {}
            for lang in _LATIN_LANG:
                score = 0.0

                special_chars = _LATIN_SPECIAL_CHARS.get(lang, ())
                if special_chars:
                    special_count = _count_special_chars(clean_text, special_chars)
                    score += special_count * 10.0

                keywords = _LATIN_KEYWORDS.get(lang, ())
                if keywords:
                    keyword_count = _count_keywords(clean_text, keywords)
                    score += keyword_count * 1.0

                if score > 0:
                    scores[lang] = score

            if scores:
                max_score = max(scores.values())
                if max_score > 0:
                    for lang in scores:
                        result[lang] = min(scores[lang] / max_score, 1.0)

    if not result:
        return {}

    sorted_items = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_items)
