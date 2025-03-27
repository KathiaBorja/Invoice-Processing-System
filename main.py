import functions as fn
import pandas as pd
import os
from sqlalchemy import create_engine
import time

batch_size = 14  # Number of invoices per batch
batch_count = 0  # Batch counter

# Create an empty DataFrame to store all invoices
df = pd.DataFrame()

# Iterate through all folders inside the "invoices" folder
for folder in sorted(os.listdir("./invoices")):
    folder_path = os.path.join("./invoices/", folder)

    # Iterate through all files inside the folder
    for file_index, file in enumerate(os.listdir(folder_path)):
        pdf_path = os.path.join(folder_path, file)

        print(f"📄 Processing invoice: {pdf_path}")

        unstructured_text = fn.extract_pdf_text(pdf_path)

        print(f"📌 Extracted data type: {type(unstructured_text)}")
        print(f"📌 Extracted content: {unstructured_text}")

        if isinstance(unstructured_text, list):
            unstructured_text = " ".join(str(item) for item in unstructured_text)
        elif isinstance(unstructured_text, dict):
            unstructured_text = str(unstructured_text)

        # Structure the text from the invoice
        structured_text = fn.structure_text(unstructured_text)

        # Ensure the structured text is a string
        if structured_text != "error":
            structured_text = str(structured_text)  # Convert to string if it's not already
            
            if isinstance(structured_text, str):
                invoice_df = fn.csv_to_dataframe(structured_text)
                df = pd.concat([df, invoice_df], ignore_index=True)
            else:
                print(f"⚠️ The structured text from {pdf_path} is not a valid string.")
        else:
            print(f"⚠️ The structured text from {pdf_path} is invalid: {structured_text}")
        
        # Process a batch
        if (file_index + 1) % batch_size == 0:
            batch_count += 1
            print(f"✅ Batch {batch_count} processed. Pausing to avoid exceeding API limits...")
            time.sleep(60)  # Pause for 60 seconds between batches to avoid exceeding API request limits

print(df.head())  
print(df.dtypes)  # Display the data types of each column
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")