from pdf2image import convert_from_path
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from weasyprint import HTML
import base64
import os
import PyPDF2
import re

PDF_HEADINGS = ["SUMMARY", "EFFECTIVE DATE", "UNSAFE CONDITION", "COMPLIANCE"]
# PDF_HEADINGS = ["SUMMARY", "EFFECTIVE DATE", "COMPLIANCE"]

def convert_html_to_pdf(file_path, target_string, dest_path):
    with open(file_path, "r", encoding="utf-8") as html_file:
        lines = html_file.readlines()

    start_index = next((i for i, line in enumerate(lines) if target_string in line), 0)

    ad_html_content = "".join(lines[start_index:])

    file_name = os.path.basename(file_path).rsplit('.', 1)[0] + ".pdf"
    pdf_file_path = os.path.join(dest_path, file_name)

    HTML(string=ad_html_content).write_pdf(pdf_file_path)
    print(f"Converted AD to PDF: {pdf_file_path}")

    return pdf_file_path


def pdf_to_png(pdf_path, output_path):
    # Convert PDF to a list of images
    images = convert_from_path(pdf_path)
    
    # Combine images vertically
    widths, heights = zip(*(i.size for i in images))
    
    total_height = sum(heights)
    max_width = max(widths)
    
    combined_image = Image.new('RGB', (max_width, total_height))
    
    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height
    
    # Save combined image as a PNG
    combined_image.save(output_path, 'PNG')
    print(f"Converted PDF to PNG as {output_path}")

    # Verify the saved image format
    with Image.open(output_path) as img:
        print(f"Image format: {img.format}")

    # Check file size
    file_size = os.path.getsize(output_path)
    print(f"Compressed image size: {file_size / (1024 * 1024):.2f} MB")

    return output_path


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def extract_text_by_headings(pdf_path, headings=PDF_HEADINGS):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        extracted_content = {heading: [] for heading in headings}
        heading_patterns = {heading: re.compile(r'\b' + re.escape(heading) + r'\b', re.IGNORECASE) for heading in headings}

        current_heading = None
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            lines = text.split('\n')

            for line in lines:
                matched_heading = None
                for heading, pattern in heading_patterns.items():
                    if pattern.search(line):
                        matched_heading = heading
                        break

                if matched_heading:
                    current_heading = matched_heading
                elif current_heading:
                    extracted_content[current_heading].append(line)
    
    return extracted_content


def create_pdf_from_headings(output_path, extracted_content):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    y = height - 40  # Start from top of the page
    for heading, content in extracted_content.items():
        if content:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(30, y, heading)
            y -= 20
            
            c.setFont("Helvetica", 10)
            for line in content:
                c.drawString(30, y, line)
                y -= 15
                if y < 40:  # If the space is running out, create a new page
                    c.showPage()
                    y = height - 40
            y -= 30
    
    c.save()

def process_pdf(pdf_path, output_path, headings=PDF_HEADINGS):
    extracted_content = extract_text_by_headings(pdf_path, headings)
    create_pdf_from_headings(output_path, extracted_content)
