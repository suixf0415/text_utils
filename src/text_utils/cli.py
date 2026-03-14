"""Command-line interface for text processing tools."""

import argparse
import sys
from typing import Optional

from text_utils import cleaner, formatter, regex_tool


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="texttool", description="Text processing CLI tool"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean whitespace from text")
    clean_parser.add_argument("input", nargs="?", help="Input text (or use stdin)")
    clean_parser.add_argument(
        "--strip",
        action="store_true",
        default=True,
        help="Strip leading/trailing whitespace",
    )
    clean_parser.add_argument(
        "--collapse", action="store_true", default=True, help="Collapse multiple spaces"
    )
    clean_parser.add_argument(
        "--remove-newlines", action="store_true", help="Remove newline characters"
    )
    clean_parser.add_argument("-i", "--input-file", help="Input file")
    clean_parser.add_argument("-o", "--output-file", help="Output file")

    # Strip command
    strip_parser = subparsers.add_parser(
        "strip", help="Strip leading/trailing whitespace"
    )
    strip_parser.add_argument("input", nargs="?", help="Input text")
    strip_parser.add_argument("-i", "--input-file", help="Input file")
    strip_parser.add_argument("-o", "--output-file", help="Output file")

    # Collapse spaces command
    collapse_parser = subparsers.add_parser("collapse", help="Collapse multiple spaces")
    collapse_parser.add_argument("input", nargs="?", help="Input text")
    collapse_parser.add_argument("-i", "--input-file", help="Input file")
    collapse_parser.add_argument("-o", "--output-file", help="Output file")

    # Remove newlines command
    rmnl_parser = subparsers.add_parser("rmnl", help="Remove newline characters")
    rmnl_parser.add_argument("input", nargs="?", help="Input text")
    rmnl_parser.add_argument("-i", "--input-file", help="Input file")
    rmnl_parser.add_argument("-o", "--output-file", help="Output file")

    # Normalize whitespace command
    norm_parser = subparsers.add_parser("normalize", help="Normalize all whitespace")
    norm_parser.add_argument("input", nargs="?", help="Input text")
    norm_parser.add_argument("-i", "--input-file", help="Input file")
    norm_parser.add_argument("-o", "--output-file", help="Output file")

    # Remove empty lines command
    rmempty_parser = subparsers.add_parser("rmempty", help="Remove empty lines")
    rmempty_parser.add_argument("input", nargs="?", help="Input text")
    rmempty_parser.add_argument("-i", "--input-file", help="Input file")
    rmempty_parser.add_argument("-o", "--output-file", help="Output file")

    # Format commands
    upper_parser = subparsers.add_parser("upper", help="Convert to uppercase")
    upper_parser.add_argument("input", nargs="?", help="Input text")
    upper_parser.add_argument("-i", "--input-file", help="Input file")
    upper_parser.add_argument("-o", "--output-file", help="Output file")

    lower_parser = subparsers.add_parser("lower", help="Convert to lowercase")
    lower_parser.add_argument("input", nargs="?", help="Input text")
    lower_parser.add_argument("-i", "--input-file", help="Input file")
    lower_parser.add_argument("-o", "--output-file", help="Output file")

    title_parser = subparsers.add_parser("title", help="Convert to title case")
    title_parser.add_argument("input", nargs="?", help="Input text")
    title_parser.add_argument("-i", "--input-file", help="Input file")
    title_parser.add_argument("-o", "--output-file", help="Output file")

    camel_parser = subparsers.add_parser("camel", help="Convert to camelCase")
    camel_parser.add_argument("input", nargs="?", help="Input text")
    camel_parser.add_argument("-i", "--input-file", help="Input file")
    camel_parser.add_argument("-o", "--output-file", help="Output file")

    snake_parser = subparsers.add_parser("snake", help="Convert to snake_case")
    snake_parser.add_argument("input", nargs="?", help="Input text")
    snake_parser.add_argument("-i", "--input-file", help="Input file")
    snake_parser.add_argument("-o", "--output-file", help="Output file")

    kebab_parser = subparsers.add_parser("kebab", help="Convert to kebab-case")
    kebab_parser.add_argument("input", nargs="?", help="Input text")
    kebab_parser.add_argument("-i", "--input-file", help="Input file")
    kebab_parser.add_argument("-o", "--output-file", help="Output file")

    constant_parser = subparsers.add_parser("constant", help="Convert to CONSTANT_CASE")
    constant_parser.add_argument("input", nargs="?", help="Input text")
    constant_parser.add_argument("-i", "--input-file", help="Input file")
    constant_parser.add_argument("-o", "--output-file", help="Output file")

    # Regex commands
    grep_parser = subparsers.add_parser(
        "grep", help="Search for lines matching pattern"
    )
    grep_parser.add_argument("pattern", help="Regular expression pattern")
    grep_parser.add_argument("input", nargs="?", help="Input text")
    grep_parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="Ignore case"
    )
    grep_parser.add_argument("-v", "--invert", action="store_true", help="Invert match")
    grep_parser.add_argument("--input-file", help="Input file")
    grep_parser.add_argument("--output-file", help="Output file")

    replace_parser = subparsers.add_parser("replace", help="Replace pattern with text")
    replace_parser.add_argument("pattern", help="Regular expression pattern")
    replace_parser.add_argument(
        "replacement", help="Replacement text", nargs="?", default=""
    )
    replace_parser.add_argument("input", nargs="?", help="Input text")
    replace_parser.add_argument(
        "-c", "--count", type=int, default=0, help="Max replacements"
    )
    replace_parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="Ignore case"
    )
    replace_parser.add_argument("--input-file", help="Input file")
    replace_parser.add_argument("--output-file", help="Output file")

    extract_parser = subparsers.add_parser("extract", help="Extract matches from text")
    extract_parser.add_argument("pattern", help="Regular expression pattern")
    extract_parser.add_argument("input", nargs="?", help="Input text")
    extract_parser.add_argument(
        "-g", "--group", type=int, default=0, help="Capture group"
    )
    extract_parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="Ignore case"
    )
    extract_parser.add_argument("--input-file", help="Input file")
    extract_parser.add_argument("--output-file", help="Output file")

    return parser


def get_input_text(args: argparse.Namespace) -> str:
    """Get input text from args (file, positional arg, or stdin)."""
    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            return f.read()
    if args.input is not None:
        return args.input
    return sys.stdin.read()


def write_output(text: str, output_file: Optional[str]) -> None:
    """Write output to file or stdout."""
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "clean":
            text = get_input_text(args)
            result = cleaner.clean_text(
                text,
                strip=args.strip,
                collapse=args.collapse,
                rm_newlines=args.remove_newlines,
            )
            write_output(result, args.output_file)

        elif args.command == "strip":
            text = get_input_text(args)
            result = cleaner.strip_whitespace(text)
            write_output(result, args.output_file)

        elif args.command == "collapse":
            text = get_input_text(args)
            result = cleaner.collapse_spaces(text)
            write_output(result, args.output_file)

        elif args.command == "rmnl":
            text = get_input_text(args)
            result = cleaner.remove_newlines(text)
            write_output(result, args.output_file)

        elif args.command == "normalize":
            text = get_input_text(args)
            result = cleaner.normalize_whitespace(text)
            write_output(result, args.output_file)

        elif args.command == "rmempty":
            text = get_input_text(args)
            result = cleaner.remove_empty_lines(text)
            write_output(result, args.output_file)

        elif args.command == "upper":
            text = get_input_text(args)
            result = formatter.to_upper(text)
            write_output(result, args.output_file)

        elif args.command == "lower":
            text = get_input_text(args)
            result = formatter.to_lower(text)
            write_output(result, args.output_file)

        elif args.command == "title":
            text = get_input_text(args)
            result = formatter.to_title(text)
            write_output(result, args.output_file)

        elif args.command == "camel":
            text = get_input_text(args)
            result = formatter.to_camel_case(text)
            write_output(result, args.output_file)

        elif args.command == "snake":
            text = get_input_text(args)
            result = formatter.to_snake_case(text)
            write_output(result, args.output_file)

        elif args.command == "kebab":
            text = get_input_text(args)
            result = formatter.to_kebab_case(text)
            write_output(result, args.output_file)

        elif args.command == "constant":
            text = get_input_text(args)
            result = formatter.to_constant_case(text)
            write_output(result, args.output_file)

        elif args.command == "grep":
            text = get_input_text(args)
            result = regex_tool.grep(
                args.pattern,
                text,
                ignore_case=getattr(args, "ignore_case", False),
                invert=getattr(args, "invert", False),
            )
            write_output("\n".join(result), args.output_file)

        elif args.command == "replace":
            text = get_input_text(args)
            result = regex_tool.replace(
                args.pattern,
                text,
                args.replacement,
                count=getattr(args, "count", 0),
                ignore_case=getattr(args, "ignore_case", False),
            )
            write_output(result, args.output_file)

        elif args.command == "extract":
            text = get_input_text(args)
            result = regex_tool.extract(
                args.pattern,
                text,
                group=getattr(args, "group", 0),
                ignore_case=getattr(args, "ignore_case", False),
            )
            write_output("\n".join(result), args.output_file)

        else:
            parser.print_help()
            return 1

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
