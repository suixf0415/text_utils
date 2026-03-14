"""Tests for text cleaning utilities."""

from text_utils import cleaner


class TestStripWhitespace:
    """Tests for strip_whitespace function."""

    def test_strip_basic(self):
        assert cleaner.strip_whitespace("  hello  ") == "hello"

    def test_strip_leading_only(self):
        assert cleaner.strip_whitespace("  hello") == "hello"

    def test_strip_trailing_only(self):
        assert cleaner.strip_whitespace("hello  ") == "hello"

    def test_strip_no_change(self):
        assert cleaner.strip_whitespace("hello") == "hello"

    def test_strip_tabs_newlines(self):
        assert cleaner.strip_whitespace("\thello\n") == "hello"


class TestCollapseSpaces:
    """Tests for collapse_spaces function."""

    def test_collapse_multiple_spaces(self):
        assert cleaner.collapse_spaces("hello    world") == "hello world"

    def test_collapse_multiple_spaces_middle(self):
        assert cleaner.collapse_spaces("hello    world    test") == "hello world test"

    def test_collapse_single_space(self):
        assert cleaner.collapse_spaces("hello world") == "hello world"

    def test_collapse_tabs(self):
        assert cleaner.collapse_spaces("hello\tworld") == "hello\tworld"


class TestRemoveNewlines:
    """Tests for remove_newlines function."""

    def test_remove_single_newline(self):
        assert cleaner.remove_newlines("hello\nworld") == "hello world"

    def test_remove_multiple_newlines(self):
        assert cleaner.remove_newlines("hello\n\n\nworld") == "hello world"

    def test_remove_crlf(self):
        assert cleaner.remove_newlines("hello\r\nworld") == "hello world"

    def test_remove_custom_replacement(self):
        assert cleaner.remove_newlines("hello\nworld", replacement="-") == "hello-world"


class TestNormalizeWhitespace:
    """Tests for normalize_whitespace function."""

    def test_normalize_basic(self):
        assert cleaner.normalize_whitespace("  hello   world  ") == "hello world"

    def test_normalize_newlines(self):
        assert cleaner.normalize_whitespace("hello\nworld") == "hello world"

    def test_normalize_mixed(self):
        assert cleaner.normalize_whitespace("  hello \n  world  \n") == "hello world"


class TestRemoveEmptyLines:
    """Tests for remove_empty_lines function."""

    def test_remove_empty_lines_basic(self):
        text = "hello\n\nworld"
        assert cleaner.remove_empty_lines(text) == "hello\nworld"

    def test_remove_multiple_empty_lines(self):
        text = "hello\n\n\n\nworld"
        assert cleaner.remove_empty_lines(text) == "hello\nworld"

    def test_remove_lines_with_spaces(self):
        text = "hello\n   \nworld"
        assert cleaner.remove_empty_lines(text) == "hello\nworld"

    def test_no_empty_lines(self):
        text = "hello\nworld"
        assert cleaner.remove_empty_lines(text) == "hello\nworld"


class TestStripLines:
    """Tests for strip_lines function."""

    def test_strip_lines_basic(self):
        text = "  hello  \n  world  "
        assert cleaner.strip_lines(text) == "hello\nworld"

    def test_strip_lines_mixed(self):
        text = "\thello\nworld\t\n"
        assert cleaner.strip_lines(text) == "hello\nworld\n"


class TestRemoveLineBreaks:
    """Tests for remove_line_breaks function."""

    def test_remove_line_breaks_basic(self):
        assert cleaner.remove_line_breaks("hello\nworld") == "hello world"

    def test_remove_line_breaks_custom(self):
        assert (
            cleaner.remove_line_breaks("hello\nworld", replacement="-") == "hello-world"
        )


class TestTruncateWhitespace:
    """Tests for truncate_whitespace function."""

    def test_truncate_basic(self):
        assert (
            cleaner.truncate_whitespace("hello    world", max_consecutive=1)
            == "hello world"
        )

    def test_truncate_allow_two(self):
        assert (
            cleaner.truncate_whitespace("hello    world", max_consecutive=2)
            == "hello  world"
        )

    def test_truncate_no_change(self):
        assert (
            cleaner.truncate_whitespace("hello world", max_consecutive=2)
            == "hello world"
        )


class TestCleanText:
    """Tests for clean_text function."""

    def test_clean_text_default(self):
        result = cleaner.clean_text("  hello   world  ")
        assert result == "hello world"

    def test_clean_text_strip_only(self):
        result = cleaner.clean_text("  hello world  ", strip=True, collapse=False)
        assert result == "hello world"

    def test_clean_text_collapse_only(self):
        result = cleaner.clean_text("hello    world", strip=False, collapse=True)
        assert result == "hello world"

    def test_clean_text_no_strip(self):
        result = cleaner.clean_text("  hello world  ", strip=False, collapse=True)
        assert result == " hello world "

    def test_clean_text_rm_newlines(self):
        result = cleaner.clean_text(
            "hello\nworld", strip=False, collapse=False, rm_newlines=True
        )
        assert result == "hello world"
