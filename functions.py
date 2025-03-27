from google import genai
import fitz  # PyMuPDF
from dotenv import load_dotenv
import os
import pandas as pd
from io import StringIO
from prompt1 import prompt1

# Load environment variables from the .env file
load_dotenv(".env")

# Retrieve the GenAI API key from the environment variables
GENAI_API_KEY = os.getenv("GENAI_API_KEY")


def extract_pdf_text(pdf_path):
    """
    Extracts text from the PDF files using PyMuPDF.
    """
    try:
        doc = fitz.open(pdf_path)  # Open the PDF
        text = "\n".join([page.get_text("text") for page in doc])  # Extract text
        return text
    except Exception as e:
        print(f"❌ Error extracting text from PDF {pdf_path}: {e}")
        return ""


def structure_text(text):
    """
    Sends the extracted text from a PDF to the GenAI model (gemini-2.0-flash)
    to convert it into a structured CSV format.
    """
    try:
        # Ensure the text is a string
        text = str(text).strip()

        # Configure the GenAI client
        client = genai.Client(api_key=GENAI_API_KEY)

        # Configure the content to send to the API
        content = [
            {
                "role": "system",
                "content": (
                    "You are an expert in invoice data extraction. Return only the CSV with the following columns: "
                    "date;supplier;expense_type;amount"
                    "Do not include explanations or repeated headers. If you cannot extract data, return 'error'."
                ),
            },
            {
                "role": "user",
                "content": f"{prompt1}\n This is the text to parse:\n{text}",
            },
        ]

        # Call the GenAI API
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=(content[0]['content'], content[1]['content']),
        )

        # Verify that the response is not empty
        if not response or not hasattr(response, "candidates"):
            print("⚠️ The API response is empty or has no candidates.")
            return "error"

        # Extract the text from the first response
        csv_text = response.candidates[0].content.parts[0].text

        print(f"📌 Generated CSV: {csv_text}")  # Debugging

        return csv_text.strip() if csv_text else "error"

    except Exception as e:
        print(f"❌ Error calling the GenAI API: {e}")
        return "error"


def csv_to_dataframe(csv):
    """Converts CSV text into a pandas DataFrame, ensuring 'amount' is numeric."""
    
    if not csv or csv.strip().lower() == "error":
        print("⚠️ Could not convert the CSV to DataFrame because the API returned 'error' or the data is empty.")
        return pd.DataFrame()  # Returns an empty DataFrame to avoid errors

    try:
        # Attempt to read the CSV with delimiter ";"
        df_temp = pd.read_csv(StringIO(csv), sep=";", skipinitialspace=True, on_bad_lines='skip', encoding="utf-8")

        # Check columns and content before returning
        print(f"📌 Detected columns: {df_temp.columns}")
        print(f"📌 First rows:\n{df_temp.head()}")

        # Verify if 'amount' is in the columns
        if "amount" not in df_temp.columns:
            print(f"⚠️ The generated CSV does not have the 'amount' column. Columns received: {df_temp.columns}")
            return df_temp
        
        # Clean and convert 'amount' to numeric
        df_temp["amount"] = pd.to_numeric(df_temp["amount"].astype(str).str.replace(",", "."), errors="coerce")

        return df_temp

    except Exception as e:
        print(f"❌ Error reading the CSV: {e}")
        return pd.DataFrame()  # Returns an empty DataFrame