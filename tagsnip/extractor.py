import re
from pathlib import Path

class TagsnipError(RuntimeError):
    pass

def marker_matches(line: str, marker: str) -> bool:
    pattern = rf"{re.escape(marker)}(?!\S)"
    return re.search(pattern, line) is not None

def extract_tagged_block(text: str, tag: str):
    start_marker = f"tagsnip-start {tag}"
    end_marker = f"tagsnip-end {tag}"

    lines = text.splitlines()

    start_index = None
    end_index = None

    for i, line in enumerate(lines):
        if marker_matches(line, start_marker):
            if start_index is not None:
                raise TagsnipError(f"Multiple start tags found for '{tag}'")

            start_index = i

    if start_index is None:
        raise TagsnipError(f"Start tag not found for '{tag}'")
    
    for i in range(start_index + 1, len(lines)):
        if marker_matches(lines[i], end_marker):
            end_index = i
            break

    if end_index is None:
        raise TagsnipError(f"End tag not found for '{tag}'")
    
    return "\n".join(lines[start_index + 1:end_index]), start_index + 2, end_index

def extract_from_file(path: str | Path, tag: str) -> str:
    file_path = Path(path)

    if not file_path.is_file():
        raise TagsnipError(f"File not found: {file_path}")
    
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TagsnipError(f"Could not read file: {file_path}") from exc

    return extract_tagged_block(text, tag)
