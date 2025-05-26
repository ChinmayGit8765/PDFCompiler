import os
import zipfile
from PyPDF2 import PdfMerger
import tempfile
import sys

def combine_pdfs_from_zip(zip_path, output_pdf):
    # Extract PDFs from ZIP file to temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)
            print(f"Extracted to temporary directory: {tmpdirname}")

        # Initialize PDF merger
        merger = PdfMerger()

        # Find and sort all PDFs in temporary directory
        pdf_files = []
        for root, _, files in os.walk(tmpdirname):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))

        pdf_files.sort()

        if not pdf_files:
            print("No PDF files found in ZIP.")
            return

        # Append all PDFs to merger
        for pdf in pdf_files:
            print(f"Merging: {pdf}")
            merger.append(pdf)

        # Write combined PDF
        merger.write(output_pdf)
        merger.close()
        print(f"Combined PDF created: {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pdf_combiner.exe <path_to_zip_file> <output_pdf_name>")
    else:
        zip_path = sys.argv[1]
        output_pdf = sys.argv[2] if sys.argv[2].lower().endswith('.pdf') else sys.argv[2] + '.pdf'
        combine_pdfs_from_zip(zip_path, output_pdf)
