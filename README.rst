PDFPipe
=======================

A command-line tool in Python. Pass it one or more text files, or pipe something from stdin, and it will
produce a text-only PDF file.

Handy for quickly printing plain text content in a clean and predictable format. Specify font, font size,
orientation and paper size from the command line.

Installation
------------
Grab the file pdfpipe.py and execute it, or:

::

   pip install pdfpipe

Or, you can download the source and

::

   python setup.py install

or

::

    sudo python setup.py install

if required.

Command-Line Usage
------------------

In your command-line:

::

   echo "Hello from a PDF file named output.pdf" | pdfpipe

Or

::

   pdfpipe -p -b -o printable.pdf -s 14 -g Letter --title "Reports for today" report*.txt

Type
::

   pdfpipe --help

for more information on the available options.

Fonts and Unicode
-----------------
The FPDF library knows about the following font families:

::

    Courier, Arial, Times, Symbol, ZapfDingbats

Which can all be chosen as the font with the -f option. By default,
Courier will be used for the monospace font, Arial (helvetica) for
proportional (-p).

If you need to print non-latin text, or want a different font for any
other reason, instead specify the full path to a TTF font file. E.g.:

::

    ./pdfpipe.py unicode_text.txt -f "/Library/Fonts/Arial Unicode.ttf"


