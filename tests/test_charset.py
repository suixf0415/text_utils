"""Tests for charset detection module."""

import pytest

from text_utils import charset


class TestDetectEncoding:
    """Tests for detect_encoding function."""

    def test_detect_utf8_ascii(self):
        """Test detecting UTF-8 with ASCII text."""
        data = b"Hello, World!"
        encoding, confidences = charset.detect_encoding(data)
        assert encoding == "utf-8"

    def test_detect_utf8_chinese(self):
        """Test detecting UTF-8 with Chinese text."""
        data = "你好世界".encode("utf-8")
        encoding, confidences = charset.detect_encoding(data)
        assert encoding == "utf-8"

    def test_detect_gbk(self):
        """Test detecting GBK encoding."""
        data = "你好".encode("gbk")
        encoding, confidences = charset.detect_encoding(data)
        assert encoding in ["gbk", "gb2312"]

    def test_detect_gb2312(self):
        """Test detecting GB2312 encoding."""
        data = "中国".encode("gb2312")
        encoding, confidences = charset.detect_encoding(data)
        assert encoding in ["gbk", "gb2312"]

    def test_detect_big5(self):
        """Test detecting Big5 encoding."""
        data = "你好".encode("big5")
        encoding, confidences = charset.detect_encoding(data)
        assert encoding == "big5"

    def test_detect_iso8859_1(self):
        """Test detecting ISO-8859-1 encoding."""
        data = "Hello World".encode("iso-8859-1")
        encoding, confidences = charset.detect_encoding(data)
        assert encoding in ["utf-8", "iso-8859-1"]

    def test_detect_windows1252(self):
        """Test detecting Windows-1252 encoding."""
        data = "café".encode("windows-1252")
        encoding, confidences = charset.detect_encoding(data)
        assert encoding in ["utf-8", "windows-1252", "iso-8859-1"]

    def test_detect_shift_jis(self):
        """Test detecting Shift_JIS encoding."""
        data = "こんにちは".encode("shift_jis")
        encoding, confidences = charset.detect_encoding(data)
        assert encoding in ["shift_jis", "gbk"]

    def test_detect_euc_kr(self):
        """Test detecting EUC-KR encoding."""
        data = "안녕하세요".encode("euc-kr")
        encoding, confidences = charset.detect_encoding(data)
        assert encoding in ["euc-kr", "gbk"]

    def test_detect_empty_bytes(self):
        """Test detecting empty bytes returns None."""
        data = b""
        encoding, confidences = charset.detect_encoding(data)
        assert encoding is None

    def test_confidences_dict(self):
        """Test that confidences dict is returned."""
        data = b"Hello"
        encoding, confidences = charset.detect_encoding(data)
        assert isinstance(confidences, dict)
        assert len(confidences) > 0


class TestConvertEncoding:
    """Tests for convert_encoding function."""

    def test_convert_gbk_to_utf8(self):
        """Test converting GBK to UTF-8."""
        data = "你好".encode("gbk")
        result = charset.convert_encoding(data, "gbk", "utf-8")
        assert result == "你好"

    def test_convert_utf8_to_utf8(self):
        """Test converting UTF-8 to UTF-8."""
        data = "Hello".encode("utf-8")
        result = charset.convert_encoding(data, "utf-8", "utf-8")
        assert result == "Hello"

    def test_convert_big5_to_utf8(self):
        """Test converting Big5 to UTF-8."""
        data = "你好".encode("big5")
        result = charset.convert_encoding(data, "big5", "utf-8")
        assert result == "你好"

    def test_convert_iso8859_to_utf8(self):
        """Test converting ISO-8859-1 to UTF-8."""
        data = "café".encode("iso-8859-1")
        result = charset.convert_encoding(data, "iso-8859-1", "utf-8")
        assert result == "café"
