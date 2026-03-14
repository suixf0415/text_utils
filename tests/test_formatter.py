"""Tests for text formatting utilities."""

from text_utils import formatter


class TestUpperLower:
    """Tests for uppercase and lowercase conversion."""

    def test_to_upper(self):
        assert formatter.to_upper("hello world") == "HELLO WORLD"

    def test_to_upper_already(self):
        assert formatter.to_upper("HELLO") == "HELLO"

    def test_to_lower(self):
        assert formatter.to_lower("HELLO WORLD") == "hello world"

    def test_to_lower_already(self):
        assert formatter.to_lower("hello") == "hello"


class TestTitleSentence:
    """Tests for title and sentence case."""

    def test_to_title(self):
        assert formatter.to_title("hello world") == "Hello World"

    def test_to_title_already(self):
        assert formatter.to_title("Hello World") == "Hello World"

    def test_to_sentence(self):
        assert formatter.to_sentence("hello world") == "Hello world"

    def test_to_sentence_all_caps(self):
        assert formatter.to_sentence("HELLO WORLD") == "Hello world"


class TestCamelCase:
    """Tests for camelCase conversion."""

    def test_camel_simple(self):
        assert formatter.to_camel_case("hello world") == "helloWorld"

    def test_camel_snake(self):
        assert formatter.to_camel_case("hello_world") == "helloWorld"

    def test_camel_kebab(self):
        assert formatter.to_camel_case("hello-world") == "helloWorld"

    def test_camel_mixed(self):
        assert formatter.to_camel_case("HelloWorld") == "helloWorld"

    def test_camel_already(self):
        assert formatter.to_camel_case("helloWorld") == "helloWorld"

    def test_camel_empty(self):
        assert formatter.to_camel_case("") == ""


class TestPascalCase:
    """Tests for PascalCase conversion."""

    def test_pascal_simple(self):
        assert formatter.to_pascal_case("hello world") == "HelloWorld"

    def test_pascal_snake(self):
        assert formatter.to_pascal_case("hello_world") == "HelloWorld"

    def test_pascal_camel(self):
        assert formatter.to_pascal_case("helloWorld") == "HelloWorld"

    def test_pascal_empty(self):
        assert formatter.to_pascal_case("") == ""


class TestSnakeCase:
    """Tests for snake_case conversion."""

    def test_snake_simple(self):
        assert formatter.to_snake_case("hello world") == "hello_world"

    def test_snake_camel(self):
        assert formatter.to_snake_case("helloWorld") == "hello_world"

    def test_snake_pascal(self):
        assert formatter.to_snake_case("HelloWorld") == "hello_world"

    def test_snake_kebab(self):
        assert formatter.to_snake_case("hello-world") == "hello_world"

    def test_snake_upper(self):
        assert formatter.to_snake_case("HELLO WORLD") == "hello_world"


class TestKebabCase:
    """Tests for kebab-case conversion."""

    def test_kebab_simple(self):
        assert formatter.to_kebab_case("hello world") == "hello-world"

    def test_kebab_snake(self):
        assert formatter.to_kebab_case("hello_world") == "hello-world"

    def test_kebab_camel(self):
        assert formatter.to_kebab_case("helloWorld") == "hello-world"

    def test_kebab_upper(self):
        assert formatter.to_kebab_case("HELLO WORLD") == "hello-world"


class TestConstantCase:
    """Tests for CONSTANT_CASE conversion."""

    def test_constant_simple(self):
        assert formatter.to_constant_case("hello world") == "HELLO_WORLD"

    def test_constant_snake(self):
        assert formatter.to_constant_case("hello_world") == "HELLO_WORLD"

    def test_constant_camel(self):
        assert formatter.to_constant_case("helloWorld") == "HELLO_WORLD"


class TestDotCase:
    """Tests for dot.case conversion."""

    def test_dot_simple(self):
        assert formatter.to_dot_case("hello world") == "hello.world"

    def test_dot_snake(self):
        assert formatter.to_dot_case("hello_world") == "hello.world"

    def test_dot_camel(self):
        assert formatter.to_dot_case("helloWorld") == "hello.world"


class TestInvertCase:
    """Tests for case inversion."""

    def test_invert_mixed(self):
        assert formatter.invert_case("Hello World") == "hELLO wORLD"

    def test_invert_all_lower(self):
        assert formatter.invert_case("hello") == "HELLO"

    def test_invert_all_upper(self):
        assert formatter.invert_case("HELLO") == "hello"


class TestCapitalizeWords:
    """Tests for capitalizing words."""

    def test_capitalize_words_basic(self):
        assert formatter.capitalize_words("hello world") == "Hello World"

    def test_capitalize_words_with_exceptions(self):
        result = formatter.capitalize_words("the quick brown fox", exceptions=["the"])
        assert result == "the Quick Brown Fox"

    def test_capitalize_words_multiple_exceptions(self):
        result = formatter.capitalize_words(
            "the and or a in", exceptions=["a", "and", "or", "in"]
        )
        assert result == "The and or a in"
