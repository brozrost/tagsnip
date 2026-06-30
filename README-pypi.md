`tagsnip` is a Python CLI tool for extracting tagged code snippets from local files or remote URLs, such as GitHub raw files. It serves as the backend for the tagsnip LaTeX package and enables dynamic inclusion of code snippets directly in LaTeX documents.

<div align="center">
  <a href="https://github.com/brozrost/tagsnip/actions">
    <img src="https://github.com/brozrost/tagsnip/actions/workflows/python-package.yml/badge.svg">
  </a>
  <a href="https://github.com/brozrost/tagsnip/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/brozrost/tagsnip">
  </a>
  <a href="https://github.com/brozrost/tagsnip/issues">
    <img src="https://img.shields.io/github/issues/brozrost/tagsnip">
  </a>
  <a href="https://github.com/brozrost/tagsnip/pulls">
    <img src="https://img.shields.io/github/issues-pr/brozrost/tagsnip">
  </a>
</div>

## Installation

Install `tagsnip` from PyPI:

```sh
pip install tagsnip
```

After installation, the command `tagsnip` should be available in your shell:

```sh
tagsnip --help
```

## Usage

```sh
tagsnip -s <source> -t <tag> [-o <output>]
```

```sh
tagsnip -c <output>
```

### Command-line options
```text
-s, --source   Local file path or remote URL.  
-t, --tag      Snippet tag to extract.  
-o, --output   Optional output file path.
-c, --cleanup  Removes temporary files at specified path. 
```

`--source` and `--tag` are mandatory arguments. If `--output` is provided, `tagsnip` writes the extracted snippet to the selected file. Otherwise, the snippet is written to `stdout`.

When `--output` is used, `tagsnip` also writes a metadata file next to the output file. For example, if the output file is `snippet.tmp`, then the metadata file is `snippet.tmp.meta`. Both files can be removed using the `--cleanup` option.
 
The metadata file contains the original start and end line numbers of the extracted snippet. This is used by the LaTeX package to preserve source line numbering.

### Supported sources 

- Local text files
- Remote text files available over HTTP or HTTPS
- GitHub raw file URLs

### Tag format

`tagsnip` extracts code between two matching markers:

```text
tagsnip-start <tag>
...
tagsnip-end <tag>
```

Tags are case-sensitive. Markers must appear on separate lines. The tag must follow the marker name after one space.

For example:

```python
# tagsnip-start demo
print("This line will be extracted.")
# tagsnip-end demo
```

The marker lines themselves are not included in the extracted snippet.

### Error handling

`tagsnip` reports errors when:

- The tag is not found
- Start/end markers are mismatched
- Multiple start markers exist
- The source cannot be fetched

## Quick example

### Example source file

```python
# tagsnip-start demo
def main():
    x = 1
    y = 2
    print(x + y)

    return 0
# tagsnip-end demo

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### CLI usage

Write the snippet to `stdout`:

```bash    
tagsnip -s example.py -t demo
```

Write the snippet to a file:
```bash  
tagsnip -s example.py -t demo -o out/out.txt
```

Get snippet from URL:
```bash
tagsnip -s https://raw.githubusercontent.com/brozrost/tagsnip/main/docs/example.py -t demo
```

Remove temporary files:
```bash
tagsnip -c out/out.txt
```

### Python usage

```python
from tagsnip import extractor

snippet = extractor.extract_from_file("example.py", "demo")
```

## Compatibility note

The Python package and the LaTeX package should be kept in sync. Backwards compatibility is not guaranteed.
