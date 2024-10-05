import PyPDF2
from reportlab.pdfgen import canvas
from io import BytesIO
from typing import List, Dict
import cv2
import numpy as np
import datetime
from reportlab.lib.utils import ImageReader

class Page:
    def __init__(self, template_pdf_path: str):
        """
        Initialize the Page with a PDF template.

        :param template_pdf_path: Path to the PDF template file.
        """
        # Load the template PDF
        self.template_pdf = PyPDF2.PdfReader(template_pdf_path)
        self.template_page = self.template_pdf.pages[0]

        # Get the size of the template page
        self.page_width = float(self.template_page.mediabox.width)
        self.page_height = float(self.template_page.mediabox.height)

        # Create a buffer for the overlay content
        self.packet = BytesIO()
        self.canvas = canvas.Canvas(self.packet, pagesize=(self.page_width, self.page_height))

    def get_page_size(self) -> tuple:
        """
        Get the size of the template page.

        :return: Tuple of (width, height) of the page.
        """
        return self.page_width, self.page_height
    
    def add_text(self, x: float, y: float, text: str, font: str = 'Helvetica', size: int = 12, text_color: tuple = (0, 0, 0)):
        """
        Add text to the page at the specified position.

        :param x: X-coordinate.
        :param y: Y-coordinate.
        :param text: Text string to add.
        :param font: Font name.
        :param size: Font size.
        """

        #convert türkish characters to latin-1
        char_map = {
            "ç": "c",
            "Ç": "C",
            "ğ": "g",
            "Ğ": "G",
            "ı": "i",
            "İ": "I",
            "ö": "o",
            "Ö": "O",
            "ş": "s",
            "Ş": "S",
            "ü": "u",
            "Ü": "U"
        }
        for key, value in char_map.items():
            text = text.replace(key, value)

        self.canvas.setFont(font, size)
        self.canvas.setFillColorRGB(text_color[0],text_color[1], text_color[2] )  # White in RGB (1, 1, 1)
        self.canvas.drawString(x, y, text)

    def add_image_from_cv2(self, image_cv2: np.ndarray, x: float, y: float, width: float = None, height: float = None):
        """
        Add an OpenCV image (NumPy array) to the page at the specified position.

        :param image_cv2: OpenCV image frame as a NumPy array.
        :param x: X-coordinate.
        :param y: Y-coordinate.
        :param width: Width of the image.
        :param height: Height of the image.
        """
        # Convert the OpenCV image (BGR) to PNG format in-memory
        _, buffer = cv2.imencode('.png', image_cv2)

        # Create a BytesIO object to store the PNG data
        image_stream = BytesIO(buffer.tobytes())

        # Create a reportlab ImageReader object from the in-memory PNG
        img_reader = ImageReader(image_stream)

        # Draw the image on the canvas at the specified position
        self.canvas.drawImage(img_reader, x, y, width=width, height=height)

    def get_merged_page(self) -> PyPDF2.PageObject:
        """
        Merge the overlay content with the template page and return the merged page.

        :return: Merged PDF page.
        """
        # Finalize the canvas and get the overlay PDF
        try:
            self.canvas.save()
            self.packet.seek(0)
            overlay_pdf = PyPDF2.PdfReader(self.packet)
            overlay_page = overlay_pdf.pages[0]
            # Merge the overlay page with the template page
            self.template_page.merge_page(overlay_page)
        except IndexError as e:
            #if no edditon is made on the canvas, then the overlay_pdf will be empty and the merge will raise an error
            pass
        
        return self.template_page

class PDF:
    def __init__(self):
        """
        Initialize the PDF object to collect pages.
        """
        self.pages: List[PyPDF2.PageObject] = []

    def add_page(self, page: Page):
        """
        Add a Page instance to the PDF.

        :param page: Page instance to add.
        """
        merged_page = page.get_merged_page()
        self.pages.append(merged_page)

    def save(self, output_pdf_path: str):
        """
        Save the collected pages into a single PDF file.

        :param output_pdf_path: Path to the output PDF file.
        """
        writer = PyPDF2.PdfWriter()
        for page in self.pages:
            writer.add_page(page)
        with open(output_pdf_path, 'wb') as f:
            writer.write(f)

# Example Usage:
# pdf = PDF()
# pages = []

# batch_size = 8
# page_count = 1
# for i in range(0, len(image_paths), batch_size):
#     batch = image_paths[i:i + batch_size]
#     print(f"Processing batch {i // batch_size + 1} with {len(batch)} images")
#     if len(batch) == 0:
#         break
    
#     page = add_image_and_return_page(image_paths=batch, shift_info="shift_info", page_no=str(page_count))
#     pages.append(page)
#     page_count += 1
    
# pdf = PDF()
# for page in pages:
#     pdf.add_page(page)
# pdf.save('output.pdf')



