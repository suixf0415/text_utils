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

    def test_collapse_fullwidth_space(self):
        assert cleaner.collapse_spaces("hello\u3000world") == "hello world"

    def test_collapse_multiple_fullwidth_spaces(self):
        assert cleaner.collapse_spaces("hello\u3000\u3000world") == "hello world"

    def test_collapse_nonbreaking_space(self):
        assert cleaner.collapse_spaces("hello\u00a0world") == "hello world"

    def test_collapse_multiple_nonbreaking_spaces(self):
        assert cleaner.collapse_spaces("hello\u00a0\u00a0world") == "hello world"

    def test_collapse_mixed_spaces(self):
        assert cleaner.collapse_spaces("hello \u3000\u00a0 world") == "hello world"

    def test_collapse_include_tabs_false(self):
        assert (
            cleaner.collapse_spaces("hello\tworld", include_tabs=False)
            == "hello\tworld"
        )

    def test_collapse_include_tabs_true(self):
        assert (
            cleaner.collapse_spaces("hello\t\tworld", include_tabs=True)
            == "hello world"
        )


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

    def test_remove_vertical_tab(self):
        assert cleaner.remove_newlines("hello\u000bworld") == "hello world"

    def test_remove_form_feed(self):
        assert cleaner.remove_newlines("hello\u000cworld") == "hello world"

    def test_remove_nel(self):
        assert cleaner.remove_newlines("hello\u0085world") == "hello world"

    def test_remove_line_separator(self):
        assert cleaner.remove_newlines("hello\u2028world") == "hello world"

    def test_remove_paragraph_separator(self):
        assert cleaner.remove_newlines("hello\u2029world") == "hello world"

    def test_remove_mixed_newlines(self):
        assert cleaner.remove_newlines("hello\n\r\u2028world") == "hello world"


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

    def test_truncate_fullwidth_space(self):
        assert (
            cleaner.truncate_whitespace("hello\u3000\u3000world", max_consecutive=1)
            == "hello world"
        )

    def test_truncate_nonbreaking_space(self):
        assert (
            cleaner.truncate_whitespace("hello\u00a0\u00a0world", max_consecutive=1)
            == "hello world"
        )

    def test_truncate_mixed_spaces(self):
        assert (
            cleaner.truncate_whitespace("hello \u3000\u00a0 world", max_consecutive=1)
            == "hello world"
        )

    def test_truncate_max_consecutive_zero(self):
        assert (
            cleaner.truncate_whitespace("hello    world", max_consecutive=0)
            == "helloworld"
        )

    def test_truncate_max_consecutive_zero_fullwidth(self):
        assert (
            cleaner.truncate_whitespace("hello\u3000world", max_consecutive=0)
            == "helloworld"
        )

    def test_truncate_max_consecutive_zero_nonbreaking(self):
        assert (
            cleaner.truncate_whitespace("hello\u00a0world", max_consecutive=0)
            == "helloworld"
        )

    def test_truncate_invalid_negative(self):
        try:
            cleaner.truncate_whitespace("hello world", max_consecutive=-1)
            assert False, "Should raise ValueError"
        except ValueError:
            pass


class TestRemoveInvisibleChars:
    """Tests for remove_invisible_chars function."""

    def test_remove_zero_width_space(self):
        assert cleaner.remove_invisible_chars("hello\u200bworld") == "helloworld"

    def test_remove_zero_width_non_joiner(self):
        assert cleaner.remove_invisible_chars("hello\u200cworld") == "helloworld"

    def test_remove_zero_width_joiner(self):
        assert cleaner.remove_invisible_chars("hello\u200dworld") == "helloworld"

    def test_remove_left_to_right_mark(self):
        assert cleaner.remove_invisible_chars("hello\u200eworld") == "helloworld"

    def test_remove_right_to_left_mark(self):
        assert cleaner.remove_invisible_chars("hello\u200fworld") == "helloworld"

    def test_remove_bom(self):
        assert cleaner.remove_invisible_chars("hello\ufeffworld") == "helloworld"

    def test_remove_soft_hyphen(self):
        assert cleaner.remove_invisible_chars("hello\u00adworld") == "helloworld"

    def test_remove_multiple_invisible(self):
        assert (
            cleaner.remove_invisible_chars("he\u200b\u200c\u200dl\u200e\u200frld")
            == "heworld"
        )

    def test_no_invisible_chars(self):
        assert cleaner.remove_invisible_chars("hello world") == "hello world"


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
