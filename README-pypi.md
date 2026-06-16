SnipTeX is a Python CLI tool for extracting tagged code snippets from local files or remote URLs, such as GitHub raw files. It serves as the backend for the SnipTeX LaTeX package and enables dynamic inclusion of code snippets directly in LaTeX documents.

<div align="center">
  <a href="https://github.com/brozrost/sniptex/actions">
    <img src="https://github.com/brozrost/sniptex/actions/workflows/python-package.yml/badge.svg">
  </a>
  <a href="https://github.com/brozrost/sniptex/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/brozrost/sniptex">
  </a>
  <a href="https://github.com/brozrost/sniptex/issues">
    <img src="https://img.shields.io/github/issues/brozrost/sniptex">
  </a>
  <a href="https://github.com/brozrost/sniptex/pulls">
    <img src="https://img.shields.io/github/issues-pr/brozrost/sniptex">
  </a>
</div>

## Installation

Install SnipTeX from PyPI:

```sh
pip install sniptex
```

After installation, the command `sniptex` should be available in your shell:

```sh
sniptex --help
```

## Usage

```sh
sniptex -s <source> -t <tag> [-o <output>]
```

### Command-line options
```text
-s, --source   Local file path or remote URL.  
-t, --tag      Snippet tag to extract.  
-o, --output   Optional output file path.  
```

`--source` and `--tag` are mandatory arguments. If `--output` is provided, SnipTeX writes the extracted snippet to the selected file. Otherwise, the snippet is written to `stdout`.

When `--output` is used, SnipTeX also writes a metadata file next to the output file. For example, if the output file is `snippet.tmp`, then the metadata file is `snippet.tmp.meta`.
 
The metadata file contains the original start and end line numbers of the extracted snippet. This is used by the LaTeX package to preserve source line numbering.

### Supported sources 

- Local text files
- Remote text files available over HTTP or HTTPS
- GitHub raw file URLs

### Tag format

SnipTeX extracts code between two matching markers:

```text
sniptex-start <tag>
...
sniptex-end <tag>
```

Tags are case-sensitive. Markers must appear on separate lines. The tag must follow the marker name after one space.

For example:

```python
# sniptex-start demo
print("This line will be extracted.")
# sniptex-end demo
```

The marker lines themselves are not included in the extracted snippet.

### Error handling

SnipTeX reports errors when:

- the tag is not found
- start/end markers are mismatched
- multiple start markers exist
- the source cannot be fetched

## Quick example

### Example source file

```python
# sniptex-start demo
def main():
    x = 1
    y = 2
    print(x + y)

    return 0
# sniptex-end demo

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### CLI usage

Write the snippet to `stdout`:

```bash    
sniptex -s example.py -t demo
```

Write the snippet to a file:
```bash  
sniptex -s example.py -t demo -o out/out.txt
```

Get snippet from URL:
```bash
sniptex -s https://raw.githubusercontent.com/brozrost/sniptex/main/docs/example.py -t demo
```


### Python usage

```python
from sniptex import extractor

snippet = extractor.extract_from_file("example.py", "demo")
```

## Compatibility note

The Python package and the LaTeX package should be kept in sync. Backwards compatibility is not guaranteed.
