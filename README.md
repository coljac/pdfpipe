# PDFPipe

A command-line tool in Python. Pass it one or more text files, or pipe something from stdin, and it will produce a text-only PDF file.

Handy for quickly printing plain text content in a clean and predictable format. Specify font, font size, orientation, and paper size from the command line.

## Installation

```
pip install pdfpipe
```

Or, you can download the source and:

```
pip install .
```

## Command-line usage

```
pdfpipe -h
```

```
pdfpipe -t "My Title" -o "output.pdf" "file1.txt" "file2.txt"
```

Or pipe something from stdin:

```
echo "Hello, world!" | pdfpipe -o "output.pdf"
```

## As a library

```
from pdfpipe import create_pdf

create_pdf(input_files=["file1.txt", "file2.txt"], title="My Title", output="output.pdf")
```

## Fonts

PDFPipe comes with a few fonts built-in, but you can also specify a custom font.

```
pdfpipe -f "customfont.ttf" -o "output.pdf" "file1.txt" "file2.txt"
```

PDFPipe comes with a few fonts built-in, but you can also specify a custom font.

```
pdfpipe -f "customfont.ttf" -o "output.pdf" "file1.txt" "file2.txt"
```

### Update

This was my first python project. Ten years later, here's an update!