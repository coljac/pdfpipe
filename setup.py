from setuptools import setup, find_packages
setup(
    name = "pdfpipe",
    version = "1.0",
    packages = find_packages(),
    scripts = ['pdfpipe.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3', 'fpdf>=1.7',],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Colin Jacobs",
    author_email = "colin@coljac.net",
    description = "Python command line tool to quickly create PDFs from text content",
    license = "Public Domain",
    keywords = "pdf command-line",
    url = "https://github.com/coljac/pdfpipe",
)
