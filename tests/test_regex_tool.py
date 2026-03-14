"""Tests for regex processing utilities."""

from text_utils import regex_tool


class TestGrep:
    """Tests for grep function."""

    def test_grep_basic(self):
        result = regex_tool.grep(r"hello", "hello world\nhello there")
        assert result == ["hello world", "hello there"]

    def test_grep_single_line(self):
        result = regex_tool.grep(r"hello", "hello world")
        assert result == ["hello world"]

    def test_grep_no_match(self):
        result = regex_tool.grep(r"foo", "hello world")
        assert result == []

    def test_grep_ignore_case(self):
        result = regex_tool.grep(r"hello", "HELLO world", ignore_case=True)
        assert result == ["HELLO world"]

    def test_grep_invert(self):
        result = regex_tool.grep(r"hello", "hello world\nfoo bar", invert=True)
        assert result == ["foo bar"]


class TestReplace:
    """Tests for replace function."""

    def test_replace_basic(self):
        result = regex_tool.replace(r"hello", "hello world", "goodbye")
        assert result == "goodbye world"

    def test_replace_multiple(self):
        result = regex_tool.replace(r"hello", "hello hello hello", "hi")
        assert result == "hi hi hi"

    def test_replace_count(self):
        result = regex_tool.replace(r"hello", "hello hello hello", "hi", count=1)
        assert result == "hi hello hello"

    def test_replace_ignore_case(self):
        result = regex_tool.replace(r"hello", "HELLO world", "hi", ignore_case=True)
        assert result == "hi world"

    def test_replace_no_match(self):
        result = regex_tool.replace(r"foo", "hello world", "bar")
        assert result == "hello world"

    def test_replace_regex_groups(self):
        result = regex_tool.replace(r"(\w+) (\w+)", "hello world", r"\2 \1")
        assert result == "world hello"


class TestExtract:
    """Tests for extract function."""

    def test_extract_basic(self):
        result = regex_tool.extract(r"\d+", "abc 123 def 456")
        assert result == ["123", "456"]

    def test_extract_no_match(self):
        result = regex_tool.extract(r"\d+", "abc def")
        assert result == []

    def test_extract_with_groups(self):
        result = regex_tool.extract(r"(\d+)-(\d+)", "123-456", group=1)
        assert result == ["123"]

    def test_extract_ignore_case(self):
        result = regex_tool.extract(r"hello", "HELLO world", ignore_case=True)
        assert result == ["HELLO"]


class TestExtractGroups:
    """Tests for extract_groups function."""

    def test_extract_groups_basic(self):
        result = regex_tool.extract_groups(r"(\d+)-(\d+)", "123-456")
        assert result == [("123", "456")]

    def test_extract_groups_multiple(self):
        result = regex_tool.extract_groups(r"(\d+)-(\d+)", "123-456 789-012")
        assert result == [("123", "456"), ("789", "012")]


class TestSplitByPattern:
    """Tests for split_by_pattern function."""

    def test_split_basic(self):
        result = regex_tool.split_by_pattern(r",\s*", "a, b, c")
        assert result == ["a", "b", "c"]

    def test_split_no_match(self):
        result = regex_tool.split_by_pattern(r"x", "abc")
        assert result == ["abc"]


class TestFindAll:
    """Tests for find_all function."""

    def test_find_all_basic(self):
        result = regex_tool.find_all(r"\d+", "abc 123 def 456")
        assert len(result) == 2
        assert result[0]["text"] == "123"
        assert result[0]["start"] == 4
        assert result[1]["text"] == "456"

    def test_find_all_positions(self):
        result = regex_tool.find_all(r"hello", "hello world hello")
        assert len(result) == 2
        assert result[0]["start"] == 0
        assert result[0]["end"] == 5
        assert result[1]["start"] == 12
        assert result[1]["end"] == 17


class TestCountMatches:
    """Tests for count_matches function."""

    def test_count_basic(self):
        count = regex_tool.count_matches(r"\d+", "abc 123 def 456")
        assert count == 2

    def test_count_no_match(self):
        count = regex_tool.count_matches(r"\d+", "abc def")
        assert count == 0


class TestIsMatch:
    """Tests for is_match function."""

    def test_is_match_true(self):
        assert regex_tool.is_match(r"hello", "hello world") is True

    def test_is_match_false(self):
        assert regex_tool.is_match(r"foo", "hello world") is False


class TestFullMatch:
    """Tests for full_match function."""

    def test_full_match_true(self):
        assert regex_tool.full_match(r"hello", "hello") is True

    def test_full_match_false(self):
        assert regex_tool.full_match(r"hello", "hello world") is False


class TestGrepWithContext:
    """Tests for grep_with_context function."""

    def test_grep_with_context_before(self):
        text = "line1\nline2\nhello\nline4\nline5"
        result = regex_tool.grep_with_context(r"hello", text, before=1)
        assert "line2" in result
        assert "hello" in result

    def test_grep_with_context_after(self):
        text = "line1\nhello\nline3\nline4\nline5"
        result = regex_tool.grep_with_context(r"hello", text, after=1)
        assert "hello" in result
        assert "line3" in result
