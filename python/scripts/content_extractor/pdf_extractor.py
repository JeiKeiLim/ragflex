""" This script contains the functions for handling PDFs.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

from scripts.content_extractor.base_extractor import BaseExtractor

import PyPDF2
import io

from typing import Union


class PDFExtractor(BaseExtractor):
    def __init__(self, path: str) -> None:
        """
        Initializes the PDFProcessor.

        Args:
            pdf_file_path: The file path to the PDF from which to extract text.
        """
        super().__init__(path)

    def _extract_content(self, pdf: Union[str, bytes]) -> str:
        """
        Extracts text from a PDF file and cleans it by removing unnecessary characters.

        Args:
            pdf_file_path: The file path to the PDF from which to extract text.

        Returns:
            The cleaned, extracted text from the PDF.
        """
        # Open the PDF file
        if isinstance(pdf, str):
            file = open(pdf, "rb")
            pdf_reader = PyPDF2.PdfReader(file)
        else:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf))

        # Initialize text storage
        text = ""
        # Iterate through each page in the PDF
        for page in pdf_reader.pages:
            # Extract text from page
            page_text = page.extract_text() if page.extract_text() else ""
            for line in page_text.split("\n"):
                cleaned_text = "".join(filter(str.isprintable, line))
                # Add cleaned text to text storage
                text += cleaned_text + "\n"
        return text
