"""Tests for language detection module."""

import pytest

from text_utils.language import (
    LANG_EN,
    LANG_JA,
    LANG_KO,
    LANG_UNKNOWN,
    LANG_ZH,
    detect_language,
    detect_language_detail,
)


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
