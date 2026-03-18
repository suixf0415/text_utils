"""Tests for language detection module."""

import pytest

from text_utils.language import *

class TestDetectLanguage:
    def test_chinese(self):
        assert detect_language("你好世界") == LANG_ZH
        assert detect_language("今天天气很好") == LANG_ZH
        assert detect_language("中文测试") == LANG_ZH

    def test_chinese_long_text(self):
        text = "人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。"
        assert detect_language(text) == LANG_ZH

    def test_chinese_poetry(self):
        text = "床前明月光，疑是地上霜。举头望明月，低头思故乡。"
        assert detect_language(text) == LANG_ZH

    def test_english(self):
        assert detect_language("Hello World") == LANG_EN
        assert detect_language("This is a test") == LANG_EN
        assert detect_language("Python programming") == LANG_EN

    def test_english_long_text(self):
        text = "Artificial intelligence is a branch of computer science that attempts to understand the essence of intelligence and produce a new kind of machine that can respond in a way similar to human intelligence."
        assert detect_language(text) == LANG_EN

    def test_japanese(self):
        assert detect_language("こんにちは") == LANG_JA
        assert detect_language("日本語を勉強します") == LANG_JA
        assert detect_language("東京") in [LANG_JA, LANG_ZH]

    def test_japanese_long_text(self):
        text = "人工知能はコンピュータ科学の一分野であり、知性の本質を把握し、人間の知性と同様の方法で反応できる新しい知性機械を生産することを目標としています。"
        assert detect_language(text) == LANG_JA

    def test_japanese_mixed_hiragana_kanji(self):
        text = "今日は良い天気ですね走出去流行病を抑え外出を控えましょう"
        assert detect_language(text) == LANG_JA

    def test_korean(self):
        assert detect_language("안녕하세요") == LANG_KO
        assert detect_language("한국어") == LANG_KO
        assert detect_language("서울") == LANG_KO

    def test_japanese_with_katakana(self):
        assert detect_language("テスト") == LANG_JA
        assert detect_language("コンピューター") == LANG_JA

    def test_empty_string(self):
        assert detect_language("") == LANG_UNKNOWN
        assert detect_language("   ") == LANG_UNKNOWN

    def test_only_punctuation(self):
        assert detect_language(".,!?;:") == LANG_UNKNOWN
        assert detect_language("，。！？；：") == LANG_UNKNOWN

    def test_mixed_chinese_english(self):
        result = detect_language("你好 Hello")
        assert result in [LANG_ZH, LANG_EN]

    def test_numbers(self):
        assert detect_language("12345") == LANG_UNKNOWN
        assert detect_language("abc123") == LANG_EN

    def test_special_chars(self):
        assert detect_language("@#$%") == LANG_UNKNOWN
        assert detect_language("test@email.com") == LANG_EN


class TestDetectLanguageDetail:
    def test_chinese_detail(self):
        result = detect_language_detail("你好世界")
        assert LANG_ZH in result
        assert result[LANG_ZH] > 0.5

    def test_chinese_long_text_detail(self):
        text = "人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。"
        result = detect_language_detail(text)
        assert LANG_ZH in result
        assert result[LANG_ZH] > 0.5

    def test_english_detail(self):
        result = detect_language_detail("Hello World")
        assert LANG_EN in result
        assert result[LANG_EN] > 0.5

    def test_english_long_text_detail(self):
        text = "Artificial intelligence is transforming the way we live and work. It has applications in many fields including healthcare, finance, and transportation."
        result = detect_language_detail(text)
        assert LANG_EN in result
        assert result[LANG_EN] > 0.5

    def test_japanese_long_text_detail(self):
        text = "人工知能は私たちの生活と仕事の仕方を変革しています。医療、金融、輸送など多くの分野に応用されています。"
        result = detect_language_detail(text)
        assert LANG_JA in result
        assert result[LANG_JA] > 0.4

    def test_empty_detail(self):
        assert detect_language_detail("") == {}
        assert detect_language_detail("   ") == {}

    def test_detail_sorted(self):
        result = detect_language_detail("你好 Hello")
        items = list(result.items())
        if len(items) > 1:
            assert items[0][1] >= items[1][1]


class TestDetectFrench:
    def test_french_special_chars(self):
        result = detect_language("été français")
        assert result in [LANG_FR, LANG_PT]

    def test_french_long_text(self):
        text = (
            "La France est un pays situé en Europe occidentale. Paris est la capitale."
        )
        result = detect_language(text)
        assert result == LANG_FR

    def test_french_very_long_text(self):
        text = """La République française est un pays d'Europe occidentale. 
        Paris est la capitale et la plus grande ville de France. 
        La France est connue pour sa cuisine, son vin, sa culture et son histoire riche. 
        Le français est la langue officielle et le français est parlé par des millions de personnes dans le monde.
        La devise de la France est Liberté, Égalité, Fraternité.
        La cuisine française est considérée comme l'une des meilleures au monde."""
        result = detect_language(text)
        assert result == LANG_FR

    def test_french_with_cedilla(self):
        result = detect_language("réçu français")
        assert result in [LANG_FR, LANG_PT]
        result = detect_language("garçon")
        assert result in [LANG_FR, LANG_PT]

    def test_french_detail_long_text(self):
        result = detect_language_detail(
            "La France est un pays situé en Europe occidentale."
        )
        assert LANG_FR in result
        assert result[LANG_FR] > 0.3


class TestDetectGerman:
    def test_german_special_chars(self):
        assert detect_language("größer") == LANG_DE
        assert detect_language("für")
        assert detect_language("straße") == LANG_DE

    def test_german_long_text(self):
        text = "Deutschland ist ein Land in Mitteleuropa. Berlin ist die Hauptstadt."
        result = detect_language(text)
        assert result in [LANG_DE, LANG_EN]

    def test_german_very_long_text(self):
        text = """Die Bundesrepublik Deutschland ist ein Staat in Mitteleuropa. 
        Berlin ist die Hauptstadt und die größte Stadt des Landes. 
        Deutschland ist bekannt für seine Industrie, seine Musik und seine Kultur. 
        Die deutsche Sprache wird von etwa 100 Millionen Menschen als Muttersprache gesprochen.
        Die Wirtschaft Deutschlands ist die größte in Europa.
        Deutsche Wissenschaftler haben viele wichtige Beiträge zur Wissenschaft geleistet."""
        result = detect_language(text)
        assert result == LANG_DE

    def test_german_umlaut(self):
        assert detect_language("Mädchen") == LANG_DE
        assert detect_language("über") == LANG_DE
        assert detect_language("Grüß Gott") == LANG_DE

    def test_german_eszett(self):
        assert detect_language("schließen") == LANG_DE
        assert detect_language("Straße") == LANG_DE

    def test_german_detail_long_text(self):
        result = detect_language_detail(
            "Die deutsche Sprache ist eine wichtige Sprache in Europa."
        )
        assert LANG_DE in result
        assert result[LANG_DE] > 0.3


class TestDetectSpanish:
    def test_spanish_special_chars(self):
        assert detect_language("español") == LANG_ES
        assert detect_language("niño") == LANG_ES

    def test_spanish_long_text(self):
        text = (
            "España es un país situado en la península ibérica. Madrid es la capital."
        )
        result = detect_language(text)
        assert result == LANG_ES

    def test_spanish_very_long_text(self):
        text = """El Reino de España es un país ubicado en Europa meridional. 
        Madrid es la capital y la ciudad más grande del país. 
        España es conocida por su clima, su gastronomía, su flamenco y sus beaches. 
        El español es la segunda lengua más hablada del mundo por número de hablantes nativos.
        La economía española es una de las más grandes de Europa.
        España tiene una rica historia y cultura que atrae a millones de visitantes cada año."""
        result = detect_language(text)
        assert result == LANG_ES

    def test_spanish_inverted_marks(self):
        assert detect_language("¿Cómo estás?") == LANG_ES
        assert detect_language("¡Hola!") == LANG_ES

    def test_spanish_tilde(self):
        assert detect_language("año") == LANG_ES
        assert detect_language("español") == LANG_ES

    def test_spanish_detail_long_text(self):
        result = detect_language_detail("El español es una lengua Romance importante.")
        assert LANG_ES in result
        assert result[LANG_ES] > 0.3


class TestDetectItalian:
    def test_italian_special_chars(self):
        result = detect_language("perché")
        assert result in [LANG_IT, LANG_ES, LANG_PT, LANG_FR]

    def test_italian_long_text(self):
        text = "L'Italia è un paese situato in Europa. Roma è la capitale."
        result = detect_language(text)
        assert result in [LANG_IT, LANG_FR]

    def test_italian_very_long_text(self):
        text = """La Repubblica Italiana è un paese situato nel sud Europa. 
        Roma è la capitale e la città più grande del paese. 
        L'Italia è conosciuta per la sua cucina, la sua arte e la sua storia. 
        La lingua italiana è parlata da circa 60 milioni di persone in tutto il mondo.
        L'economia italiana è una delle più grandi d'Europa.
        L'Italia ha dato molti contributi importanti alla cultura mondiale."""
        result = detect_language(text)
        assert result in [LANG_IT, LANG_FR]

    def test_italian_accents(self):
        result = detect_language("perché")
        assert result in [LANG_IT, LANG_ES, LANG_PT, LANG_FR]
        assert detect_language("più") == LANG_IT

    def test_italian_detail_long_text(self):
        result = detect_language_detail(
            "L'Italia è un bellissimo paese con una storia ricca."
        )
        assert LANG_IT in result
        assert result[LANG_IT] > 0.3


class TestDetectPortuguese:
    def test_portuguese_special_chars(self):
        result = detect_language("português")
        assert result in [LANG_PT, LANG_FR]

    def test_portuguese_special_chars2(self):
        result = detect_language("ação")
        assert result in [LANG_PT, LANG_ES]

    def test_portuguese_special_chars3(self):
        assert detect_language("são") == LANG_PT

    def test_portuguese_very_long_text(self):
        text = """A República Portuguesa é um país localizado no sudoeste da Europa. 
        Lisboa é a capital e a maior cidade de Portugal. 
        Portugal é conhecido pela sua história, gastronomia e belas paisagens. 
        A língua portuguesa é falada por mais de 250 milhões de pessoas em todo o mundo.
        A economia portuguesa é uma das mais antigas da Europa.
        Portugal tem uma rica tradição cultural e histórica."""
        result = detect_language(text)
        assert result == LANG_PT

    def test_portuguese_tilde(self):
        assert detect_language("ação") == LANG_PT
        assert detect_language("são") == LANG_PT
        assert detect_language("avião") == LANG_PT

    def test_portuguese_detail_long_text(self):
        result = detect_language_detail(
            "O português é uma língua importante falada em muitos países."
        )
        assert LANG_PT in result
        assert result[LANG_PT] > 0.3


class TestDetectDutch:
    def test_dutch_basic(self):
        result = detect_language("Hallo wereld")
        assert result in [LANG_NL, LANG_EN]

    def test_dutch_special_chars(self):
        assert detect_language("ijs") == LANG_NL

    def test_dutch_very_long_text(self):
        text = """Het Koninkrijk Nederland is een land in West-Europa. 
        Amsterdam is de hoofdstad en de grootste stad van het land. 
        Nederland is bekend om zijn tulpen, molens en fietsen. 
        De Nederlandse taal wordt gesproken door ongeveer 25 miljoen mensen in Nederland en België.
        De economie van Nederland is een van de sterkste in Europa.
        Nederland heeft een rijke cultuur en geschiedenis."""
        result = detect_language(text)
        assert result == LANG_NL

    def test_dutch_ij(self):
        assert detect_language("ijs") == LANG_NL
        assert detect_language("het Nederlandse ijs") == LANG_NL

    def test_dutch_detail_long_text(self):
        result = detect_language_detail(
            "Nederland is een mooi land met een rijke geschiedenis."
        )
        assert LANG_NL in result
        assert result[LANG_NL] > 0.3


class TestDetectMongolian:
    def test_mongolian_traditional(self):
        assert detect_language("ᠮᠣᠩᠭᠤᠯ") == LANG_MN
        assert detect_language("ᠮᠣᠩᠭᠣᠯᠤᠭᠴᠢ") == LANG_MN

    def test_mongolian_mixed(self):
        text = "ᠮᠣᠩᠭᠤᠯ ᠪᠠᠷᠢᠮᠲᠤᠭᠠᠢ"
        result = detect_language(text)
        assert result == LANG_MN


class TestDetectLatinLanguagesDetail:
    def test_french_detail(self):
        result = detect_language_detail("été français")
        assert LANG_FR in result

    def test_german_detail(self):
        result = detect_language_detail("für größere Straße")
        assert LANG_DE in result

    def test_spanish_detail(self):
        result = detect_language_detail("español niño")
        assert LANG_ES in result

    def test_mongolian_detail(self):
        result = detect_language_detail("ᠮᠣᠩᠭᠤᠯ")
        assert LANG_MN in result
        assert result[LANG_MN] > 0.5


class TestDetectMongolianCyrillic:
    def test_mongolian_cyrillic_basic(self):
        assert detect_language("Монгол хэл") == LANG_MN_CYRIL

    def test_mongolian_cyrillic_with_ou(self):
        assert detect_language("өдөр") == LANG_MN_CYRIL

    def test_mongolian_cyrillic_with_u(self):
        assert detect_language("үсэг") == LANG_MN_CYRIL

    def test_mongolian_cyrillic_mixed(self):
        text = "Монгол Улс бол Ази тивд байрлах улс юм"
        assert detect_language(text) == LANG_MN_CYRIL

    def test_mongolian_cyrillic_detail(self):
        result = detect_language_detail("Монгол хэл")
        assert LANG_MN_CYRIL in result
        assert result[LANG_MN_CYRIL] > 0.5
