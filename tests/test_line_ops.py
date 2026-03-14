"""Tests for line operations utilities."""

from text_utils import line_ops


class TestDeduplicate:
    """Tests for deduplicate function."""

    def test_deduplicate_basic(self):
        text = "apple\nbanana\napple\ncherry"
        result = line_ops.deduplicate(text)
        assert result == "apple\nbanana\ncherry"

    def test_deduplicate_empty(self):
        text = "a\nb\nc"
        result = line_ops.deduplicate(text)
        assert result == "a\nb\nc"

    def test_deduplicate_ignore_case(self):
        text = "apple\nApple\nAPPLE"
        result = line_ops.deduplicate(text, case_sensitive=False)
        assert result == "apple"


class TestSortLines:
    """Tests for sort_lines function."""

    def test_sort_basic(self):
        text = "banana\napple\ncherry"
        result = line_ops.sort_lines(text)
        assert result == "apple\nbanana\ncherry"

    def test_sort_reverse(self):
        text = "banana\napple\ncherry"
        result = line_ops.sort_lines(text, reverse=True)
        assert result == "cherry\nbanana\napple"

    def test_sort_numeric(self):
        text = "10\n2\n1\n20"
        result = line_ops.sort_lines(text, numeric=True)
        assert result == "1\n2\n10\n20"


class TestShuffleLines:
    """Tests for shuffle_lines function."""

    def test_shuffle_preserves_count(self):
        text = "a\nb\nc\nd\ne"
        result = line_ops.shuffle_lines(text)
        lines = result.split("\n")
        assert len(lines) == 5


class TestReverseLines:
    """Tests for reverse_lines function."""

    def test_reverse_basic(self):
        text = "a\nb\nc"
        result = line_ops.reverse_lines(text)
        assert result == "c\nb\na"


class TestFilterLines:
    """Tests for filter_lines function."""

    def test_filter_include(self):
        text = "hello\nworld\nfoo\nbar"
        result = line_ops.filter_lines(text, r"hello|world")
        assert result == "hello\nworld"

    def test_filter_exclude(self):
        text = "hello\nworld\nfoo\nbar"
        result = line_ops.filter_lines(text, r"hello|world", include=False)
        assert result == "foo\nbar"

    def test_filter_ignore_case(self):
        text = "Hello\nWORLD\nfoo"
        result = line_ops.filter_lines(text, r"hello", ignore_case=True)
        assert result == "Hello"


class TestNumberLines:
    """Tests for number_lines function."""

    def test_number_basic(self):
        text = "a\nb\nc"
        result = line_ops.number_lines(text)
        assert result == "1: a\n2: b\n3: c"

    def test_number_custom_start(self):
        text = "a\nb"
        result = line_ops.number_lines(text, start=0)
        assert result == "0: a\n1: b"

    def test_number_custom_width(self):
        text = "a\nb"
        result = line_ops.number_lines(text, width=2)
        assert result == "01: a\n02: b"


class TestUniqLines:
    """Tests for uniq_lines function."""

    def test_uniq_basic(self):
        text = "a\na\nb\nb\nb\nc"
        result = line_ops.uniq_lines(text)
        assert result == "a\nb\nc"


class TestHeadLines:
    """Tests for head_lines function."""

    def test_head_basic(self):
        text = "a\nb\nc\nd\ne"
        result = line_ops.head_lines(text, 3)
        assert result == "a\nb\nc"

    def test_head_more_than_lines(self):
        text = "a\nb"
        result = line_ops.head_lines(text, 10)
        assert result == "a\nb"


class TestTailLines:
    """Tests for tail_lines function."""

    def test_tail_basic(self):
        text = "a\nb\nc\nd\ne"
        result = line_ops.tail_lines(text, 3)
        assert result == "c\nd\ne"


class TestSliceLines:
    """Tests for slice_lines function."""

    def test_slice_basic(self):
        text = "a\nb\nc\nd\ne"
        result = line_ops.slice_lines(text, 1, 3)
        assert result == "b\nc"

    def test_slice_to_end(self):
        text = "a\nb\nc"
        result = line_ops.slice_lines(text, 1)
        assert result == "b\nc"


class TestJoinLines:
    """Tests for join_lines function."""

    def test_join_basic(self):
        text = "a\nb\nc"
        result = line_ops.join_lines(text, ",")
        assert result == "a,b,c"

    def test_join_space(self):
        text = "hello\nworld"
        result = line_ops.join_lines(text, " ")
        assert result == "hello world"


class TestCountLines:
    """Tests for count_lines function."""

    def test_count_basic(self):
        text = "a\nb\nc"
        assert line_ops.count_lines(text) == 3

    def test_count_empty(self):
        text = "a\nb"
        assert line_ops.count_lines(text, empty=True) == 0

    def test_count_all(self):
        text = "a\nb\nc"
        assert line_ops.count_lines(text) == 3
