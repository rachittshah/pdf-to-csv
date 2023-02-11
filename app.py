import streamlit as st
import pandas as pd
import pdfplumber
import re
import openai

openai.api_key = "your-openai-key"

def extract_entities(text):
    """
    Given a string of text, returns the extracted entities, such as company name, invoice number, date, 
    company tax ID, total amount with tax, total tax, currency. Numeric values do not show EUR or USD 
    symbols, and dates are in format: DD-MM-YYYY.

    Parameters:
    text (str): A string of text to be processed.

    Returns:
    dict: The extracted entities in the form of a dictionary.
    """
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt='Extract all entities company name, invoice number, date, company tax ID, total amount with tax, total tax, currency. For numeric values do not show EUR or USD symbols. dates in format: DD-MM-YYYY.\n\n###\n\n"' + text + '"',
      temperature=0.7,
      max_tokens=1438,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response

def extract_text(pdf_path):
    """
    Given the path to a PDF file, extracts the text from each page and returns it as a string.

    Parameters:
    pdf_path (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF file.
    """
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        text = ''
        for page in pages:
            text += page.extract_text()
        return text

def pdf_extractor_app():
    """
    Main function for the PDF Extractor app. Allows the user to upload a PDF file, extracts the entities 
    from the text of the PDF, and displays the extracted entities in a table.
    """
    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if pdf_file:
        text = extract_text(pdf_file)
        entities = extract_entities(text)
        df = pd.DataFrame(entities["choices"][0]["text"].splitlines(), columns=["Value"])
        st.header("Entities")
        st.table(df)
        st.header("Download")
        if st.button("Download as CSV"):
            st.write(df.to_csv(index=False), "text/csv")

pdf_files = {}

def main():
    """
    The main function of the PDF Extractor app. It contains a Streamlit title and a side menu with two options: 
    "Upload PDF" and "PDF List".
    Depending on the user's choice, it either calls the pdf_extractor_app function to upload a new PDF or allows the 
    user to select a previously uploaded PDF from the list. If no PDFs have been uploaded yet, it displays a warning.
    """
    st.title("PDF Extractor")
    menu = ["Upload PDF", "PDF List"]
    choice = st.sidebar.selectbox("Select Option", menu)
    if choice == "Upload PDF":
        pdf_extractor_app()
    elif choice == "PDF List":
        if len(pdf_files) == 0:
            st.warning("No PDFs uploaded yet")
        else:
            pdf_list = list(pdf_files.keys())
            selected_pdf = st.selectbox("Select a PDF", pdf_list)
            if selected_pdf != None:
                pdf_extractor_app(pdf_files[selected_pdf])

if __name__ == '__main__':
    main()
