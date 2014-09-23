#!/usr/bin/python
# PDFPipe
# -*- coding: latin-1 -*-
# ----------------------------------------------------------------------------
# I, Colin Jacobs, <colin@coljac.net>, the author of this file, release it
# to the public domain for use and modification without restriction. Where
# possible, retaining acknowledgement of original authorship is appreciated.
# ----------------------------------------------------------------------------
# ****************************************************************************
# * Software: PDFPipe                                                        *
# * Version:  1.0                                                            *
# * Date:     2014-09-23                                                     *
# * Last update: 2014-09-23                                                  *
# *                                                                          *
# * Author:  Colin Jacobs, colin@coljac.net                                  *
# *                                                                          *
# * Usage: Pass it one or more text files, or pipe something from stdin, and *
# * it will produce a text-only PDF file. Handy for quickly printing plain   *
# * text content in a clean and predictable format.                          *
# *                                                                          *
# * Help and options:                                                        *
# *                                                                          *
# * usage: pdfy.py [-h] [-t TITLE] [-g PAPER] [-b] [-n] [-l] [-s FONT_SIZE]  *
# *                [-o OUTPUT] [-f FONT | -m | -p]                           *
# *                [input_files [input_files ...]]                           *
# *                                                                          *
# * Create a PDF file quickly from some text.                                *
# *                                                                          *
# * positional arguments:                                                    *
# *   input_files           text file input                                  *
# *                                                                          *
# * optional arguments:                                                      *
# *   -h, --help            show this help message and exit                  *
# *   -t TITLE, --title TITLE                                                *
# *                         a title string for the document                  *
# *   -g PAPER, --paper PAPER                                                *
# *                         paper size (A4, Letter, A5, etc)                 *
# *   -b                    Add page break after each file's contents        *
# *   -n                    Add page numbers in footer                       *
# *   -l, --landscape       landscape orientation                            *
# *   -s FONT_SIZE, --font-size FONT_SIZE                                    *
# *                         font size as integer (default: 12.0)             *
# *   -o OUTPUT, --output OUTPUT                                             *
# *                         output file name (default: output.pdf            *
# *   -f FONT, --font FONT  name of font to use                              *
# *   -m, --mono            use monospace font (default)                     *
# *   -p, --proportional    use proportional font                            *
# *                                                                          *
# * Fonts and Unicode                                                        *
# * By default, the FPDF library knows about the following font families:    *
# *                                                                          *
# *             Courier, Arial, Times, Symbol, ZapfDingbats                  *
# *                                                                          *
# * By default, Courier will be used for the monospace font, Arial           *
# * (helvetica) for proportional (-p switch).                                *
# *                                                                          *
# * If you need to print non-latin text, or want a different font for any    *
# * other reason, instead specify the full path to a TTF font file. E.g.:    *
# *                                                                          *
# *     ./pdfpipe.py unicode_text.txt -f "/Library/Fonts/Arial Unicode.ttf"  *
# *                                                                          *
# * Other examples:                                                          *
# * 	                                                                     *
# *     find . | ./pdfpipe.py                                                *
# * 	                                                                     *
# * Produces an A4 PDF in 12-point Courier (monospaced) font.                *
# *                                                                          *
# *     ./pdfpipe.py -g Letter -s 10 -p --title "Daily reports" report*.txt  *
# *                                                                          *
# * Produces a Letter-sized PDF, in 10-point proportional font (Arial),      *
# * with the specified title, concatenating the text from matching files.    *
# *                                                                          *
# ****************************************************************************

# TODO
# Make usable as Python module
# Make sure default margins are ok, or allow user to set
# Centre the title
# Page number right/left for printing, or options for top/bottom

from fpdf import FPDF

# default settings
paper_size = 'A4'
font_size = 12.0
doc_title = None
page_numbers = False
page_breaks = False
output_file_name = 'output.pdf'
orientation = 'P'
pdf_font = "Courier"

class TextPDF(FPDF):
    """ FPDF library PDF object subclassed to implement headers and footers"""
    def __init__(self, orientation, format, page_nums):
        FPDF.__init__(self, orientation=orientation, unit='mm', format=format)
        self.page_nums_on = page_nums

    def footer(this):
        if this.page_nums_on:
            # Go to 1.5 cm from bottom
            this.set_y(-15)
            # Hard-code Arial as font
            this.set_font('Arial','I',8)
            # Center page number
            this.cell(0,10,'Page %s' % this.page_no(),0,0,'R')

if __name__ == "__main__":
    # Parse the command line
    import argparse
    parser = argparse.ArgumentParser(description='Create a PDF file '
                                                 'quickly from some text.')
    parser.add_argument('-t', '--title', help='a title string for the '
                                              'document',
                        default=None)
    parser.add_argument('-g', '--paper', help='paper size (A4, A3, A5, Letter, '
                                              'Legal)',
                        default=paper_size)
    parser.add_argument('-b', help='Add page break after each file\'s '
                                   'contents',
                        action='store_true', default=page_breaks)
    parser.add_argument('-n', help='Add page numbers in footer',
                        action="store_true", default=page_numbers)
    parser.add_argument('-l', "--landscape", help='landscape orientation',
                        action='store_true', default=False)
    parser.add_argument('-s', '--font-size', help='font size as integer '
                                                  '(default: ' + str(font_size) + ')',
                        default=font_size, type=int)
    parser.add_argument('-o', '--output', help='output file name '
                                               '(default: output.pdf',
                                                default=output_file_name)
    parser.add_argument('input_files', help='text file input', nargs="*")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--font', help='name of font to use')
    group.add_argument('-m', '--mono', help='use monospace font (default)',
                       default=True, action='store_true')
    group.add_argument('-p', '--proportional', help='use proportional font',
                       action='store_true', default=False)

    args = parser.parse_args()

    paper_size = args.paper
    font_size = args.font_size
    doc_title = args.title
    page_breaks = args.b
    page_numbers = args.n
    output_file_name = args.output
    if args.landscape:
        orientation = "L"
    elif args.proportional:
        pdf_font = 'Arial'
    elif args.font:
        pdf_font = args.font


    # line spacing - in mm, scaled with font_size in points
    line_spacing = font_size * .45

    # get text content for the pdf
    pdf_content = []
    text_file = None

    if len(args.input_files) > 0:
        for file in args.input_files:
            try:
                text_file = open(file, "r")
                pdf_content.append(text_file.read())
                text_file.close()
            except Exception as ex:
                print(ex)
                exit()
    else:
        import sys
        stdin = sys.stdin.read()
        pdf_content.append(stdin)

    # create PDF object
    pdf = TextPDF(orientation=orientation, format=paper_size, page_nums=page_numbers)

    pdf.add_page()

    # Fonts: Has the user specified a font file explicitly?
    if pdf_font.lower().endswith("ttf"):
        pdf.add_font('User font', '', pdf_font, uni=True)
        pdf.set_font('User font', '', font_size)
    else:
        # Assume they have specified a built-in font family
        pdf.set_font(pdf_font, '', font_size)

    # Add specified title in larget font first
    if doc_title is not None:
        pdf.set_font_size(int(font_size * 1.5))
        pdf.write(h=line_spacing*3., txt=doc_title + "\n")
        pdf.set_font_size(int(font_size))

    # for each content blob, write out as flowing text
    for p, text_block in enumerate(pdf_content):
        pdf.write(h=line_spacing,txt=text_block);
        if page_breaks and p < len(pdf_content)-1:
            pdf.add_page()
        else:
            pdf.ln(line_spacing)
            pdf.ln(line_spacing)

    # Write out the file
    pdf.output(output_file_name, 'F')
