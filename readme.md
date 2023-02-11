### PDF Extractor
This is a simple application that allows you to extract entities from a PDF file and save it in a CSV file. It uses Streamlit as the frontend and OpenAI for entity extraction.

Requirements
- Streamlit
- Pandas
- PdfPlumber
- OpenAI

You can install the required libraries by running the following command:

```pip install -r requirements.txt```

Running the application

To run the application, simply run the following command:

```streamlit run main.py```

This will open a web browser and the application will be running there. You can upload your PDF file and the extracted entities will be displayed in a table. You can also download the entities as a CSV file.

Key features
Extract entities from a PDF file such as company name, invoice number, date, company tax ID, total amount with tax, total tax, currency.
Display extracted entities in a table.
Download extracted entities as a CSV file.
