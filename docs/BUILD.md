# Building the Documentation

This directory contains the Django CMS Taxonomy documentation built with Sphinx and the Furo theme.

## Installation

Install the documentation dependencies:

```bash
pip install -r requirements.txt
```

## Building

### On macOS/Linux

```bash
make html
```

This will build the HTML documentation in the `build/html/` directory.

### On Windows

```batch
make.bat html
```

## Other Build Targets

- `make html` - Build HTML documentation
- `make clean` - Clean build artifacts
- `make latex` - Build LaTeX (for PDF)
- `make pdf` - Build PDF (if pdflatex installed)
- `make linkcheck` - Check all external links
- `make doctest` - Run doctests

## Viewing the Documentation

After building:

```bash
# Open in your browser
open build/html/index.html  # macOS
xdg-open build/html/index.html  # Linux
start build\html\index.html  # Windows
```

Or serve with Python:

```bash
cd build/html
python -m http.server 8000
# Visit http://localhost:8000
```

## Documentation Structure

The documentation follows the [Diátaxis](https://diataxis.fr/) framework:

- **`tutorials/`** - Learning-oriented guides (getting started, step-by-step)
- **`how-to/`** - Problem-solving guides (specific tasks)
- **`reference/`** - Technical reference documentation (API docs)
- **`explanation/`** - Understanding-oriented guides (concepts, design decisions)

## Configuration

The Sphinx configuration is in `source/conf.py`. Key settings:

- **Theme**: Furo (`furo`)
- **Parser**: MyST parser for Markdown support
- **Extensions**:
  - `sphinx.ext.autodoc` - Auto-document Python code
  - `sphinx.ext.intersphinx` - Link to other projects
  - `sphinx.ext.viewcode` - Link to source code
  - `sphinx.ext.napoleon` - Google-style docstrings
  - `myst_parser` - Markdown support

## Adding Documentation

1. Create a new `.md` file in the appropriate directory
2. Add it to the `toctree` in `index.md` or section index files
3. Rebuild with `make html`

## Tips

- Use relative links between docs: `[link text](../other-section/page.md)`
- Code examples automatically format with syntax highlighting
- Use triple backticks with language specification for code blocks
- MyST supports all Markdown features plus reStructuredText directives

## Troubleshooting

**"sphinx-build: command not found"**
- Install Sphinx: `pip install -r requirements.txt`

**"No module named 'furo'"**
- Install dependencies: `pip install -r requirements.txt`

**Broken links**
- Run `make linkcheck` to find broken links
- Check relative paths in toctree directives

**Markdown not rendering properly**
- Ensure MyST parser is installed
- Check that file extension is `.md`
