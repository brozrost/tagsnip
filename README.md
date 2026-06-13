### SnipTeX is a LaTeX package for including tagged code snippets from local files or remote URLs. It extracts marked sections of code and typesets them in a consistent style, supporting reproducible and maintainable documentation.

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

**Czech docs and example document:** <a href="https://github.com/brozrost/sniptex/blob/main/docs/main.pdf">main.pdf</a>

## Installation

SnipTeX consists of two parts:

1. LaTeX package `sniptex.sty`,
2. Python backend package `sniptex`.

Both parts are required.

### Installing the LaTeX package from CTAN

Download the <a href="">SnipTeX package archive from CTAN</a> and extract it. For a local project installation, copy `sniptex.sty` next to your main `.tex` file:

```sh
project/
├── main.tex
└── sniptex.sty
```

This is the simplest installation method and is sufficient for compiling a single project. For a user-wide installation, place `sniptex.sty` into your local TeX tree.

Also see: ctan url

### Installing the Python backend

SnipTeX uses a Python backend with the same name to parse source files. The backend is published on PyPI. Before using the LaTeX package, install the backend:

```sh
pip install sniptex
```

Also see: https://pypi.org/project/sniptex/

After installation, the backend must be available in the system `PATH` under the command name `sniptex`. You can check this with:

~~~sh
sniptex --help
~~~

## Compilation

```sh
lualatex --shell-escape docs/main.tex
```

## Usage

**Example document:** <a href="https://github.com/brozrost/sniptex/blob/main/docs/main.pdf">main.pdf</a>

SnipTeX defines the command `\IncludeCode`, which is used as follows:

```tex
\IncludeCode[options]{source}{tag}{language}{caption}
```

The optional argument `options` allows the user to override code formatting settings. These options are passed directly to `minted`, so they must be valid `minted` options and must be separated by commas. For example:

```tex
\IncludeCode[
  firstnumber=1,
  fontsize=\scriptsize,
  style=monokai
]{docs/example.py}{tag1}{Python}{Example snippet.}
```

The option `firstnumber=1` starts line numbering at line 1, `fontsize=\scriptsize` changes the font size, and `style=monokai` changes the syntax highlighting style.

Without changing `firstnumber`, SnipTeX preserves the original line numbers from the source file.

The mandatory argument `source` defines where the code should be loaded from. It can be either a local file path or a URL pointing to a remote text file. SnipTeX distinguishes these cases automatically.

The mandatory argument `tag` specifies the unique keyword identifying the requested snippet. A snippet is delimited in the source file by `sniptex-start` and `sniptex-end` markers:

```python
# sniptex-start tag1
def main():
    x = 1
    y = 2
    print(x + y)

    return 0
# sniptex-end tag1
```

The tag must follow the marker after exactly one space.

The mandatory argument `language` selects the programming language used for syntax highlighting.

The final argument `caption` defines the snippet caption. It may be empty, but the braces must still be written.

## Local snippet

Suppose the local file `docs/example.py` contains a function `main()` marked with the tag `tag1`, as seen above. The function can be included in the document with:

```tex
\IncludeCode{example.py}{tag1}{Python}{Úryvek 2: ...}
```

SHOWCASE

## Remote snippet

SnipTeX can also include snippets from source files available through web URLs.

For example, a snippet marked with the tag `tag2` in a remote Python file can be included as follows:

~~~tex
\IncludeCode[firstnumber=1]{https://raw.githubusercontent.com/brozrost/sniptex/main/docs/example2.py}{tag2}{Python}{Code snippet from a remote file.}
~~~

The remote file must be accessible over HTTP or HTTPS and must be readable as a plain text source file.

## Architecture

SnipTeX consists of two main parts: a LaTeX frontend package and an external backend utility written in Python.

The frontend defines the command `\IncludeCode` and handles the final typesetting of extracted snippets through the `minted` package.

The backend is responsible for accessing source files, finding marked code regions, and extracting them into temporary files.

During document compilation, the frontend uses shell escape to call the backend utility. It passes the source path or URL and the requested tag to the backend. The backend writes the extracted code to a temporary file, which is then inserted into the document and typeset by `minted`.

## Backend

The Python package `sniptex` provides a command-line interface that accepts a source file, a tag name, and an output file path.

The backend loads the source file, searches for the corresponding pair of `sniptex-start` and `sniptex-end` markers, and extracts the text between them.

The package also checks for error states, such as:

- a non-existent source file,
- an inaccessible remote file,
- a missing tag,
- a missing start or end marker,
- multiple occurrences of the same tag in one source file.

If an error is detected, the backend raises an exception. This interrupts the LaTeX compilation and prints an appropriate error message.

For local files, the backend uses Python's `pathlib` module. For tag matching, it uses `re`. For loading remote files over HTTP, it uses the `requests` library.

## Limitations

- SnipTeX requires LuaLaTeX.
- The document must be compiled with shell escape enabled, for example with `--shell-escape`.
- The Python backend must be installed and available in the system `PATH` under the command `sniptex`.
- SnipTeX depends on `minted`.
- Remote source files must be accessible over HTTP or HTTPS.
- Remote source files must be plain text files.

## Security note

SnipTeX requires shell escape because it calls an external Python backend during compilation and removes temporary files (lines 80, 93, and 94 in `sniptex.sty`).

Only compile trusted documents with shell escape enabled.

---
Copyright (c) 2026 Rostislav Brož.

> SnipTeX is distributed under the MIT License. The full license text is included in the repository in the [`LICENSE`](https://github.com/brozrost/sniptex/blob/main/LICENSE.md) file.