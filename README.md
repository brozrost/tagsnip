### `tagsnip` is a LaTeX package for including tagged code snippets from local files or remote URLs. It extracts marked sections of code and typesets them in a consistent style, supporting reproducible and maintainable documentation.

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

**Documentation:** <a href="https://github.com/brozrost/tagsnip/blob/main/docs/tagsnip-docs.pdf">tagsnip-docs.pdf</a>  
**Czech documentation:** <a href="https://github.com/brozrost/tagsnip/blob/main/docs/tagsnip-docs-czech.pdf">tagsnip-docs-czech.pdf</a>

> The documentation files also double as example documents for `tagsnip`.

## Installation

`tagsnip` consists of two parts:

1. LaTeX package `tagsnip.sty`,
2. Python backend package `tagsnip`.

Both parts are required.

### Installing the LaTeX package from CTAN

Download the <a href="https://ctan.org/pkg/tagsnip">`tagsnip` package archive from CTAN</a> and extract it. For a local project installation, copy `tagsnip.sty` next to your main `.tex` file:

```sh
project/
├── main.tex
└── tagsnip.sty
```

This is the simplest installation method and is sufficient for compiling a single project. For a user-wide installation, place `tagsnip.sty` into your local TeX tree.

Also see: https://ctan.org/pkg/tagsnip

### Installing the Python backend

`tagsnip` uses a Python backend with the same name to parse source files. The backend is published on PyPI. Before using the LaTeX package, install the backend:

```sh
pip install tagsnip
```

Also see: https://pypi.org/project/tagsnip/

After installation, the backend must be available in the system `PATH` under the command name `tagsnip`. You can check this with:

~~~sh
tagsnip --help
~~~

## Compilation

```sh
lualatex --shell-escape docs/tagsnip-docs.tex
```

## Usage

**Example document:** <a href="https://github.com/brozrost/tagsnip/blob/main/docs/docs.pdf">docs.pdf</a>

`tagsnip` defines the command `\IncludeCode`, which is used as follows:

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

Without changing `firstnumber`, `tagsnip` preserves the original line numbers from the source file.

The mandatory argument `source` defines where the code should be loaded from. It can be either a local file path or a URL pointing to a remote text file. `tagsnip` distinguishes these cases automatically.

The mandatory argument `tag` specifies the unique keyword identifying the requested snippet. A snippet is delimited in the source file by `tagsnip-start` and `tagsnip-end` markers:

```python
# tagsnip-start tag1
def main():
    x = 1
    y = 2
    print(x + y)

    return 0
# tagsnip-end tag1
```

The tag must follow the marker after exactly one space.

The mandatory argument `language` selects the programming language used for syntax highlighting.

The final argument `caption` defines the snippet caption. It may be empty, but the braces must still be written.

## Local snippet

Suppose the local file `docs/example.py` contains a function `main()` marked with the tag `tag1`, as seen above. The function can be included in the document with:

```tex
\IncludeCode{example.py}{tag1}{Python}{Úryvek 2: ...}
```
<div align="center">
  <img width="835" height="265" alt="# tagsnip-start tag" src="https://github.com/user-attachments/assets/4ca1bd1a-abe8-4478-963d-15c42fbe9479" />
</div>


## Remote snippet

`tagsnip` can also include snippets from source files available through web URLs.

For example, a snippet marked with the tag `tag2` in a remote Python file can be included as follows:

```tex
\IncludeCode[firstnumber=1]{https://raw.githubusercontent.com/brozrost/tagsnip/main/docs/example2.py}{tag2}{Python}{Code snippet from a remote file.}
```

<div align="center">
<img width="833" height="324" alt="Pasted Graphic 1 2" src="https://github.com/user-attachments/assets/02dfe4b5-0340-42b1-bb25-63cc0b331827" />
</div>

The remote file must be accessible over HTTP or HTTPS and must be readable as a plain text source file.

## Architecture

`tagsnip` consists of two main parts: a LaTeX frontend package and an external backend utility written in Python.

The frontend defines the command `\IncludeCode` and handles the final typesetting of extracted snippets through the `minted` package.

The backend is responsible for accessing source files, finding marked code regions, and extracting them into temporary files.

During document compilation, the frontend uses shell escape to call the backend utility. It passes the source path or URL and the requested tag to the backend. The backend writes the extracted code to a temporary file, which is then inserted into the document and typeset by `minted`.

## Backend

The Python package `tagsnip` provides a command-line interface that accepts a source file, a tag name, and an output file path.

The backend loads the source file, searches for the corresponding pair of `tagsnip-start` and `tagsnip-end` markers, and extracts the text between them.

The package also checks for error states, such as:

- a non-existent source file,
- an inaccessible remote file,
- a missing tag,
- a missing start or end marker,
- multiple occurrences of the same tag in one source file.

If an error is detected, the backend raises an exception. This interrupts the LaTeX compilation and prints an appropriate error message.

For local files, the backend uses Python's `pathlib` module. For tag matching, it uses `re`. For loading remote files over HTTP, it uses the `requests` library.

## Limitations

- `tagsnip` requires LuaLaTeX.
- The document must be compiled with shell escape enabled, for example with `--shell-escape`.
- The Python backend must be installed and available in the system `PATH` under the command `tagsnip`.
- `tagsnip` depends on `minted`.
- Remote source files must be accessible over HTTP or HTTPS.
- Remote source files must be plain text files.

## Security note

`tagsnip` requires shell escape because it calls an external Python backend during compilation and removes temporary files (lines 80, 93, and 94 in `tagsnip.sty`).

Only compile trusted documents with shell escape enabled.

---
Copyright (c) 2026 Rostislav Brož.

> `tagsnip` is distributed under the MIT License. The full license text is included in the repository in the [`LICENSE`](https://github.com/brozrost/tagsnip/blob/main/LICENSE.md) file.
