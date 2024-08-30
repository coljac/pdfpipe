#!/usr/bin/python3
# PDFPipe
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# I, Colin Jacobs, <colin@coljac.net>, the author of this file, release it
# to the public domain for use and modification without restriction. Where
# possible, retaining acknowledgement of original authorship is appreciated.
# ----------------------------------------------------------------------------

from fpdf import FPDF

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

def create_pdf(input_files=None, title=None, paper='A4', font_size=12.0, 
               page_breaks=False, page_numbers=False, output='output.pdf', 
               font='Courier', landscape=False, open_pdf_file=False):
    orientation = 'L' if landscape else 'P'
    pdf_font = font
    if font.lower().endswith("ttf"):
        custom_font = True
    else:
        custom_font = False
        if font == 'proportional':
            pdf_font = 'Arial'

    # line spacing - in mm, scaled with font_size in points
    line_spacing = font_size * .45

    # get text content for the pdf
    pdf_content = []
    if input_files:
        for file in input_files:
            try:
                with open(file, "r") as text_file:
                    pdf_content.append(text_file.read())
            except Exception as ex:
                print(ex)
                return
    else:
        import sys
        stdin = sys.stdin.read()
        pdf_content.append(stdin)

    # create PDF object
    pdf = TextPDF(orientation=orientation, format=paper, page_nums=page_numbers)
    pdf.add_page()

    # Fonts: Has the user specified a font file explicitly?
    if custom_font:
        pdf.add_font('User font', '', pdf_font, uni=True)
        pdf.set_font('User font', '', font_size)
    else:
        # Assume they have specified a built-in font family
        pdf.set_font(pdf_font, '', font_size)

    # Add specified title in larger font first
    if title is not None:
        pdf.set_font_size(int(font_size * 1.5))
        pdf.write(h=line_spacing*3., text=title + "\n")
        pdf.set_font_size(int(font_size))

    # for each content blob, write out as flowing text
    for p, text_block in enumerate(pdf_content):
        pdf.write(h=line_spacing, txt=text_block)
        if page_breaks and p < len(pdf_content)-1:
            pdf.add_page()
        else:
            pdf.ln(line_spacing)
            pdf.ln(line_spacing)

    # Write out the file
    pdf.output(output)

    if open_pdf_file:
        import os, subprocess
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', output))
        elif os.name == 'nt':
            os.startfile(output)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', output))

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Create a PDF file quickly from some text.')
    parser.add_argument('-t', '--title', help='a title string for the document', default=None)
    parser.add_argument('-g', '--paper', help='paper size (A4, A3, A5, Letter, Legal)', default='A4')
    parser.add_argument('-b', help='Add page break after each file\'s contents', action='store_true', default=False)
    parser.add_argument('-n', help='Add page numbers in footer', action="store_true", default=False)
    parser.add_argument('-l', "--landscape", help='landscape orientation', action='store_true', default=False)
    parser.add_argument('-s', '--font-size', help='font size as integer (default: 12.0)', default=12.0, type=int)
    parser.add_argument('-o', '--output', help='output file name (default: output.pdf)', default='output.pdf')
    parser.add_argument('input_files', help='text file input', nargs="*")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--font', help='name of font to use', default='Courier')
    group.add_argument('-m', '--mono', help='use monospace font (default)', default=True, action='store_true')
    group.add_argument('-p', '--proportional', help='use proportional font', action='store_true', default=False)
    group.add_argument('-x', '--open-pdf-file', help='attempts to open the resulting file', action='store_true', default=False)
    args = parser.parse_args()

    create_pdf(input_files=args.input_files, title=args.title, paper=args.paper, font_size=args.font_size, 
               page_breaks=args.b, page_numbers=args.n, output=args.output, font=args.font, 
               landscape=args.landscape, open_pdf_file=args.open_pdf_file)

if __name__ == "__main__":
    main()

