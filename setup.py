from setuptools import setup, find_packages

setup(
    name="pdfpipe",
    version="2.0",
    packages=find_packages(),
    scripts=['pdfpipe.py'],

    install_requires=[
        'fpdf2>=2.7',
    ],

    package_data={
        '': ['*.txt', '*.md'],
    },

    # metadata for upload to PyPI
    author="Colin Jacobs",
    author_email="colin@coljac.net",
    description="Python command line tool to quickly create PDFs from text content",
    license="Public Domain",
    keywords="pdf command-line",
    url="https://github.com/coljac/pdfpipe",

    # Classifiers help users find your project by categorizing it
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    python_requires='>=3.7',

    entry_points={
        'console_scripts': [
            'pdfpipe=pdfpipe:main',
        ],
    },
)
