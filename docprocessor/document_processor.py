import fitz  # PyMuPDF
import os
import pandas as pd
import spacy
from spacy_layout import spaCyLayout
import shutil
import time
import datetime

class DocumentProcessor:

    def human_readable_time(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")


    def split_pdf_into_chunks(self, input_pdf, split_file_folder, split_size=5):

        shutil.rmtree(split_file_folder)
        os.mkdir(split_file_folder)

        doc = fitz.open(input_pdf)
        total_pages = len(doc)
        counter = 1

        for start_page in range(0, total_pages, split_size):
            end_page = min(start_page + split_size, total_pages)  # Avoid out of range
            output_pdf_path = f"{split_file_folder}/split_{counter}.pdf"

            new_pdf = fitz.open()
            new_pdf.insert_pdf(doc, from_page=start_page, to_page=end_page - 1)
            new_pdf.save(output_pdf_path)
            new_pdf.close()

            counter += 1

        print("completed split_pdf_into_chunks - ", self.human_readable_time())


    def append_table_as_json_in_text(self, df: pd.DataFrame) -> str:
        table_json = df.to_json(orient='records')
        return table_json


    def proces_single_document(self, split_file_folder, pdf_file_name):
        nlp = spacy.load("en_core_web_sm")
        layout = spaCyLayout(nlp, display_table=self.append_table_as_json_in_text)
        doc = layout(split_file_folder+pdf_file_name)
        return doc.text


    def process_all_documents(self, split_file_folder, output_file):
        if os.path.exists(output_file):
            os.remove(output_file)

        pdf_files = sorted([f for f in os.listdir(split_file_folder) if f.endswith(".pdf")],
                           key=lambda x: int(x.split("_")[1].split(".")[0]))

        with open(output_file, 'w') as output_file_write:
            for filename in pdf_files:
                if filename.endswith(".pdf"):
                    pdf_file_name = os.path.join(split_file_folder, filename)
                    print(f"Processing file: {pdf_file_name} - {self.human_readable_time()}")
                    text = self.proces_single_document(split_file_folder, filename)
                    output_file_write.write(text + '\n\n')


def main():
    documentProcessor = DocumentProcessor()
    print("Started Executing document processor - ", documentProcessor.human_readable_time())
    input_pdf = "C:/Users/work/RAG/inputFiles/424B5_doc.pdf"
    split_file_folder = "C:/Users/work/RAG/inputFiles/424B5/"
    output_file= "C:/Users/work/RAG/outputFiles/424B5_output.txt"
    documentProcessor.split_pdf_into_chunks(input_pdf, split_file_folder, split_size=5)
    documentProcessor.process_all_documents(split_file_folder, output_file)
    print("completed Executing document processor - ", documentProcessor.human_readable_time())


if __name__ == "__main__":
    main()