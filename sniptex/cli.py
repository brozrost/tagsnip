import sys
import argparse
from pathlib import Path

from sniptex import extractor
from sniptex import fetcher
from sniptex import validate

def cleanup_generated_files(output_path: str) -> None:
    snippet_path = Path(output_path)
    meta_path = Path(str(snippet_path) + ".meta")

    for path in (snippet_path, meta_path):
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        except OSError as exc:
            raise RuntimeError(f"Error: Could not remove temporary file: {path}") from exc

def main() -> int:
    parser = argparse.ArgumentParser(
        description="SnipTeX is a Python package for extracting tagged code snippets " \
        "from local files or remote sources.",
        usage="""
        sniptex --help

        sniptex --source <file path> --tag <tag>
            sniptex -s example.py -t demo

        sniptex --source <file path> --tag <tag> --out <out file path>
            sniptex -s example.py -t demo -o out/out.txt

        sniptex --source <url> --tag <tag>
            sniptex -s https://raw.githubusercontent.com/brozrost/sniptex/main/docs/example.py -t demo

        sniptex --cleanup <generated file path>
            sniptex --cleanup out/out.txt
        """
    )

    parser.add_argument(
        "-s", "--source", 
        help="Path to a local file or URL"
    )
    parser.add_argument(
        "-t", "--tag", 
        help="Snippet tag name."
    )
    parser.add_argument(
        "-o", "--out", 
        help="Path to the output file. If omitted, prints to stdout."
    )

    parser.add_argument(
        "-c", "--cleanup",
        metavar="FILE",
        help="Remove a generated snippet file and its .meta file."
    )

    args = parser.parse_args()

    if args.cleanup:
        try:
            cleanup_generated_files(args.cleanup)
        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        
        return 0

    if not args.source or not args.tag:
        parser.error("Error: Arguments -s/--source and -t/--tag are required unless --cleanup is used.")


    try:
        if validate.is_url(args.source):
            fetch = fetcher.FetcherClient()
            text = fetch.fetch_text(args.source)
        else:
            text = Path(args.source).read_text(encoding="utf-8")

        snippet, first_line_num, last_line_num = extractor.extract_tagged_block(text, args.tag)

    except fetcher.FetcherError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError:
        print(f"Error: Could not read file: {args.source}", file=sys.stderr)
        return 1
    except extractor.SniptexError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.out:
        output_path = Path(args.out)
    
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(snippet, encoding="utf-8")

            meta_path = Path(str(output_path) + ".meta")
            meta_path.write_text(f"{first_line_num}\n{last_line_num}", encoding="utf-8")
        except OSError as exc:
            print(f"Error: Could not write file: {output_path}")
            return 1
    else:
        print(snippet)

    return 0

if __name__ == "__main__":
    sys.exit(main())