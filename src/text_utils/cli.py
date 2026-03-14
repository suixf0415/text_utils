"""Command-line interface for text processing tools."""

import argparse
import sys
from typing import Optional

from text_utils import cleaner, formatter, regex_tool, line_ops, extractor


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

    # Line operation commands
    dedup_parser = subparsers.add_parser("dedup", help="Remove duplicate lines")
    dedup_parser.add_argument("input", nargs="?", help="Input text")
    dedup_parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="Ignore case when comparing"
    )
    dedup_parser.add_argument("--input-file", help="Input file")
    dedup_parser.add_argument("--output-file", help="Output file")

    sort_parser = subparsers.add_parser("sort", help="Sort lines")
    sort_parser.add_argument("input", nargs="?", help="Input text")
    sort_parser.add_argument(
        "-r", "--reverse", action="store_true", help="Sort in reverse order"
    )
    sort_parser.add_argument(
        "-n", "--numeric", action="store_true", help="Sort numerically"
    )
    sort_parser.add_argument("--input-file", help="Input file")
    sort_parser.add_argument("--output-file", help="Output file")

    shuffle_parser = subparsers.add_parser("shuffle", help="Randomly shuffle lines")
    shuffle_parser.add_argument("input", nargs="?", help="Input text")
    shuffle_parser.add_argument("--input-file", help="Input file")
    shuffle_parser.add_argument("--output-file", help="Output file")

    reverse_parser = subparsers.add_parser("reverse", help="Reverse line order")
    reverse_parser.add_argument("input", nargs="?", help="Input text")
    reverse_parser.add_argument("--input-file", help="Input file")
    reverse_parser.add_argument("--output-file", help="Output file")

    filter_parser = subparsers.add_parser("filter", help="Filter lines by pattern")
    filter_parser.add_argument("pattern", help="Regular expression pattern")
    filter_parser.add_argument("input", nargs="?", help="Input text")
    filter_parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="Ignore case"
    )
    filter_parser.add_argument(
        "-v", "--invert", action="store_true", help="Invert match"
    )
    filter_parser.add_argument("--input-file", help="Input file")
    filter_parser.add_argument("--output-file", help="Output file")

    number_parser = subparsers.add_parser("number", help="Add line numbers")
    number_parser.add_argument("input", nargs="?", help="Input text")
    number_parser.add_argument(
        "-s", "--start", type=int, default=1, help="Starting number"
    )
    number_parser.add_argument(
        "-w", "--width", type=int, default=0, help="Number width"
    )
    number_parser.add_argument("--input-file", help="Input file")
    number_parser.add_argument("--output-file", help="Output file")

    # Extraction commands
    email_parser = subparsers.add_parser("email", help="Extract email addresses")
    email_parser.add_argument("input", nargs="?", help="Input text")
    email_parser.add_argument("--input-file", help="Input file")
    email_parser.add_argument("--output-file", help="Output file")

    phone_parser = subparsers.add_parser("phone", help="Extract phone numbers")
    phone_parser.add_argument("input", nargs="?", help="Input text")
    phone_parser.add_argument(
        "-r", "--region", default="cn", choices=["cn", "us"], help="Phone region"
    )
    phone_parser.add_argument("--input-file", help="Input file")
    phone_parser.add_argument("--output-file", help="Output file")

    url_parser = subparsers.add_parser("url", help="Extract URLs")
    url_parser.add_argument("input", nargs="?", help="Input text")
    url_parser.add_argument("--input-file", help="Input file")
    url_parser.add_argument("--output-file", help="Output file")

    id_parser = subparsers.add_parser("idcard", help="Extract ID card numbers (China)")
    id_parser.add_argument("input", nargs="?", help="Input text")
    id_parser.add_argument("--input-file", help="Input file")
    id_parser.add_argument("--output-file", help="Output file")

    hashtag_parser = subparsers.add_parser("hashtag", help="Extract hashtags")
    hashtag_parser.add_argument("input", nargs="?", help="Input text")
    hashtag_parser.add_argument("--input-file", help="Input file")
    hashtag_parser.add_argument("--output-file", help="Output file")

    mention_parser = subparsers.add_parser("mention", help="Extract @mentions")
    mention_parser.add_argument("input", nargs="?", help="Input text")
    mention_parser.add_argument("--input-file", help="Input file")
    mention_parser.add_argument("--output-file", help="Output file")

    ip_parser = subparsers.add_parser("ip", help="Extract IP addresses")
    ip_parser.add_argument("input", nargs="?", help="Input text")
    ip_parser.add_argument("-4", "--ipv4", action="store_true", help="IPv4 only")
    ip_parser.add_argument("-6", "--ipv6", action="store_true", help="IPv6 only")
    ip_parser.add_argument("--input-file", help="Input file")
    ip_parser.add_argument("--output-file", help="Output file")

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

        elif args.command == "dedup":
            text = get_input_text(args)
            result = line_ops.deduplicate(
                text, case_sensitive=not getattr(args, "ignore_case", False)
            )
            write_output(result, args.output_file)

        elif args.command == "sort":
            text = get_input_text(args)
            result = line_ops.sort_lines(
                text,
                reverse=getattr(args, "reverse", False),
                numeric=getattr(args, "numeric", False),
            )
            write_output(result, args.output_file)

        elif args.command == "shuffle":
            text = get_input_text(args)
            result = line_ops.shuffle_lines(text)
            write_output(result, args.output_file)

        elif args.command == "reverse":
            text = get_input_text(args)
            result = line_ops.reverse_lines(text)
            write_output(result, args.output_file)

        elif args.command == "filter":
            text = get_input_text(args)
            result = line_ops.filter_lines(
                text,
                args.pattern,
                include=not getattr(args, "invert", False),
                ignore_case=getattr(args, "ignore_case", False),
            )
            write_output(result, args.output_file)

        elif args.command == "number":
            text = get_input_text(args)
            result = line_ops.number_lines(
                text, start=getattr(args, "start", 1), width=getattr(args, "width", 0)
            )
            write_output(result, args.output_file)

        elif args.command == "email":
            text = get_input_text(args)
            result = extractor.extract_emails(text)
            write_output("\n".join(result), args.output_file)

        elif args.command == "phone":
            text = get_input_text(args)
            result = extractor.extract_phones(
                text, region=getattr(args, "region", "cn")
            )
            write_output("\n".join(result), args.output_file)

        elif args.command == "url":
            text = get_input_text(args)
            result = extractor.extract_urls(text)
            write_output("\n".join(result), args.output_file)

        elif args.command == "idcard":
            text = get_input_text(args)
            result = extractor.extract_id_cards(text)
            write_output("\n".join(result), args.output_file)

        elif args.command == "hashtag":
            text = get_input_text(args)
            result = extractor.extract_hashtags(text)
            write_output("\n".join(result), args.output_file)

        elif args.command == "mention":
            text = get_input_text(args)
            result = extractor.extract_mentions(text)
            write_output("\n".join(result), args.output_file)

        elif args.command == "ip":
            text = get_input_text(args)
            ipv4_only = getattr(args, "ipv4", False)
            ipv6_only = getattr(args, "ipv6", False)
            if ipv4_only:
                result = extractor.extract_ipv4(text)
            elif ipv6_only:
                result = extractor.extract_ipv6(text)
            else:
                result = extractor.extract_ipv4(text) + extractor.extract_ipv6(text)
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
