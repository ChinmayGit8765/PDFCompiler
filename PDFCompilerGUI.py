import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import zipfile
import os
import tempfile

def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
    if filepath:
        zip_entry.delete(0, tk.END)
        zip_entry.insert(0, filepath)

def combine_pdfs_from_zip(zip_path, output_name):
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdirname)

            merger = PdfMerger()
            pdf_files = []

            for root, _, files in os.walk(tmpdirname):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))

            if not pdf_files:
                messagebox.showerror("Error", "No PDF files found in the ZIP archive.")
                return

            pdf_files.sort()
            for pdf in pdf_files:
                merger.append(pdf)

            output_pdf = output_name if output_name.lower().endswith('.pdf') else output_name + '.pdf'
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=output_pdf,
                                                     filetypes=[("PDF files", "*.pdf")])
            if save_path:
                merger.write(save_path)
                merger.close()
                messagebox.showinfo("Success", f"Combined PDF saved as:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

def on_compile():
    zip_path = zip_entry.get()
    output_name = name_entry.get().strip()

    if not zip_path or not os.path.isfile(zip_path):
        messagebox.showwarning("Warning", "Please select a valid ZIP file.")
        return
    if not output_name:
        messagebox.showwarning("Warning", "Please enter a name for the output PDF.")
        return

    combine_pdfs_from_zip(zip_path, output_name)

# GUI Setup
root = tk.Tk()
root.title("PDF Combiner from ZIP")
root.geometry("500x200")
root.resizable(False, False)

tk.Label(root, text="ZIP File:").pack(pady=5)
zip_frame = tk.Frame(root)
zip_frame.pack()
zip_entry = tk.Entry(zip_frame, width=50)
zip_entry.pack(side=tk.LEFT, padx=5)
browse_button = tk.Button(zip_frame, text="Browse", command=browse_file)
browse_button.pack(side=tk.LEFT)

tk.Label(root, text="Output PDF Name:").pack(pady=5)
name_entry = tk.Entry(root, width=50)
name_entry.pack(pady=5)

compile_button = tk.Button(root, text="Compile PDF", command=on_compile, bg="lightblue", width=20)
compile_button.pack(pady=15)

root.mainloop()
