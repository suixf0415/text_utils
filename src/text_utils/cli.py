"""Command-line interface for text processing tools."""

import argparse
import sys
from typing import Optional

from text_utils import cleaner


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
