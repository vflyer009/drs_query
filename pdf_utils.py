from weasyprint import HTML
import os


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

def cleanup_html_file(file_path):
    os.remove(file_path)