import PyPDF2
import os


directory_path = "Data"

for root, dirs, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(root, file)

        with open(file_path, "rb") as data:
            pdffile_reader = PyPDF2.PdfReader(data)
            x = len(pdffile_reader.pages)
            print('x: ', x)
            page_obj = pdffile_reader.pages[x-1]
            text = page_obj.extract_text()

            file1 = open(r"./Text")
            file1.writelines(text)
            file1.close()