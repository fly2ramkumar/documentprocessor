import spacy
import pandas as pd
from spacy_layout import spaCyLayout

class DocProcessor:
    input_pdf = "C:/Users/work/RAG/inputFiles/424B5/split_1.pdf"


    def append_table_as_json_in_text(self, df: pd.DataFrame) -> str:
        table_json = df.to_json(orient='records')
        return table_json


    def load_pdf_into_spacy(self):
        nlp = spacy.load("en_core_web_sm")
        layout = spaCyLayout(nlp, display_table=self.append_table_as_json_in_text)
        doc = layout(self.input_pdf)
        return doc


    def process(self):

        page_data = {}

        doc = self.load_pdf_into_spacy()

        #print(doc.text)
        for page_layout, spans in doc._.pages:
            print(f"Page Number: {page_layout.page_no}")
            #print(f"Page Size: {page_layout.width}x{page_layout.height} pixels")

            # Extract text from spans
            page_text = ""
            for span in spans:
                if span not in doc._.tables and  span.label_ not in ["section_header", "title"]:
                    page_text += span.text + " "

            #print(f"Page Text: {page_text}")

            # Extract titles (assuming titles are spans with a specific layout)
            titles = [span.text for span in spans if span.label_ in ["section_header", "title"]]
            #print(f"Page Titles: {titles}")

            tables = [span.text for span in spans if span.label_ in ["table"]]
            #print(f"Page Tables: {tables}")

            page_data[page_layout.page_no] = {
                'title': titles,
                'text': page_text,
                'tables': tables
            }

        return page_data


def main():
    docProcessor = DocProcessor()
    page_data = docProcessor.process()
    print(page_data)


if __name__ == "__main__":
    main()