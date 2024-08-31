import os
import logging
import argparse
from PyPDF2 import PdfReader
from ebooklib import epub
from bs4 import BeautifulSoup
from docx import Document
import re

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("file_renaming.log"),
        logging.StreamHandler()
    ]
)

def get_pdf_title(file_path):
    """ Extrae el título de un archivo PDF. """
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            info = reader.metadata
            return info.get('/Title', 'NoTitleFound')
    except Exception as e:
        logging.error(f"Error al leer el PDF {file_path}: {e}")
        return "NoTitleFound"

def get_epub_title(file_path):
    """ Extrae el título de un archivo EPUB. """
    try:
        book = epub.read_epub(file_path)
        metadata_title = book.get_metadata('DC', 'title')
        if metadata_title and metadata_title[0] != "":
            return metadata_title[0][0]
        for item in book.items:
            if item.get_type() == 'text':
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    return title_tag.get_text(strip=True)
    except Exception as e:
        logging.error(f"Error al leer el EPUB {file_path}: {e}")
        return "NoTitleFound"

def get_docx_title(file_path):
    """ Extrae el título de un archivo DOCX. """
    try:
        doc = Document(file_path)
        return doc.core_properties.title if doc.core_properties.title else "NoTitleFound"
    except Exception as e:
        logging.error(f"Error al leer el DOCX {file_path}: {e}")
        return "NoTitleFound"

def sanitize_filename(filename):
    """ Sanitiza el nombre de archivo. """
    if not isinstance(filename, str):
        logging.warning(f"Se recibió un valor no string para el nombre de archivo: {filename}")
        return "InvalidFilename"
    return re.sub(r'[<>:"/\\|?*]', '_', filename)[:255]

def ensure_renamed_directory(directory):
    """ Crea el directorio 'renamed' si no existe. """
    renamed_dir = os.path.join(directory, "renamed")
    os.makedirs(renamed_dir, exist_ok=True)
    return renamed_dir

def get_unique_filename(directory, filename):
    """ Genera un nombre de archivo único. """
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base} ({counter}){extension}"
        counter += 1
    return new_filename

def rename_files_in_directory(directory):
    """ Renombra archivos en el directorio especificado. """
    renamed_dir = ensure_renamed_directory(directory)
    files = [filename for filename in os.listdir(directory) if filename.endswith(('.pdf', '.epub', '.docx'))]
    total_files = len(files)

    successful_renames = 0
    failed_renames = 0

    for index, filename in enumerate(files, start=1):
        file_path = os.path.join(directory, filename)
        logging.info(f"Procesando archivo {filename} ({index} de {total_files})")

        if filename.endswith('.pdf'):
            title = get_pdf_title(file_path)
        elif filename.endswith('.epub'):
            title = get_epub_title(file_path)
        elif filename.endswith('.docx'):
            title = get_docx_title(file_path)
        else:
            continue

        if title != "NoTitleFound":
            sanitized_title = sanitize_filename(title)
            new_filename = f"{sanitized_title}{os.path.splitext(filename)[1]}"
            new_file_path = os.path.join(renamed_dir, get_unique_filename(renamed_dir, new_filename))

            try:
                os.rename(file_path, new_file_path)
                logging.info(f'Renombrado "{filename}" a "{os.path.basename(new_file_path)}"')
                successful_renames += 1
            except PermissionError as e:
                logging.error(f'Permiso denegado al renombrar "{filename}": {e}')
                failed_renames += 1
            except OSError as e:
                logging.error(f'Error al renombrar "{filename}": {e}')
                failed_renames += 1
            except Exception as e:
                logging.error(f'Error inesperado al renombrar "{filename}": {e}')
                failed_renames += 1
        else:
            logging.info(f'No se pudo encontrar el título para "{filename}"')
            failed_renames += 1

    return successful_renames, failed_renames

def main():
    """ Función principal. """
    parser = argparse.ArgumentParser(description='Renombrar archivos PDF, EPUB y DOCX')
    parser.add_argument('directory', type=str, help='Directorio de los archivos')
    args = parser.parse_args()

    directory = args.directory
    successful_renames, failed_renames = rename_files_in_directory(directory)

    logging.info(f"Proceso completado.")
    logging.info(f"Archivos renombrados correctamente: {successful_renames}")
    logging.info(f"Archivos con errores: {failed_renames}")

if __name__ == "__main__":
    main()