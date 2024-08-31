# eBook Renamer

This project provides a Python script to automatically rename PDF, EPUB, and DOCX files in a directory based on their embedded titles. The script extracts the title metadata from each file and renames the file accordingly. It uses the PyPDF2 library for PDF files, the ebooklib and BeautifulSoup libraries for EPUB files, and the python-docx library for DOCX files. The process is logged in a log file and output to the console for real-time monitoring.

## Features

- Extracts titles from PDF, EPUB, and DOCX files.
- Renames files based on extracted titles.
- Sanitizes filenames to ensure they are valid.
- Handles file name conflicts by generating unique names.
- Logs the renaming process to both a log file and the console.

## Requirements

- Python 3.x
- The following Python libraries:
  - PyPDF2
  - ebooklib
  - beautifulsoup4
  - python-docx

You can install the required libraries using pip:

```bash
pip install PyPDF2 ebooklib beautifulsoup4 python-docx
```

## Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/book-renamer.git
```

2. Navigate to the project directory:

```bash
cd book-renamer
```

3. Run the script, passing the directory containing your books as an argument:

```bash
python rename_books.py "C:\path\to\your\book\folder"
```

This will rename all PDF and EPUB files in the specified directory based on their embedded titles.

## Logging

- The script logs its actions to a file named file_renaming.log in the project directory.
- Logs are also output to the console for real-time monitoring.
- Errors and issues during the renaming process are captured and logged for review.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue if you have suggestions for improvements or new features.

## License

This project is licensed under the MIT License.
