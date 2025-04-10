# 🧾 Invoice Processing Automation System

This project automates the extraction and processing of invoice data using AI, Python, and Power BI. It's designed to simulate a real-world business environment where companies handle large volumes of invoices and need a reliable system to digitize and analyze them efficiently.

---

## 💡 Project Overview

Invoices are often received in PDF format, making manual data entry slow and error-prone. This system solves that by:

- Extracting text from PDF invoices using PyMuPDF.
- Using a Gemini AI model to structure unstructured invoice text into a clean CSV format.
- Converting the CSV into a structured pandas DataFrame.
- Storing and processing the data for visualization in Power BI.

The final dashboard provides insights into supplier expenses, spending trends, and invoice categories — enabling companies to make data-driven decisions in finance and operations.

---

## 📂 Repository Contents

| File                          | Description                                         |
|-------------------------------|-----------------------------------------------------|
| `functions.py`                | Contains core functions for PDF parsing, AI extraction, and CSV conversion |
| `main.py`                     | Main script to process batches of invoice PDFs      |
| `InvoiceGenerator.ipynb`      | Notebook for generating or testing invoice input    |
| `prompt1.py`                  | Detailed instructions (prompt) used by the AI model |
| `invoices.db`                 | Optional SQLite database (if integration is extended) |
| `ExpenseTracking-7deOro.pbix` | Power BI dashboard to visualize extracted data      |

---

## ⚙️ Technologies Used

- **Python**
  - `PyMuPDF` for PDF text extraction
  - `pandas` for data processing
  - `sqlalchemy` for optional database integration
- **Google Gemini API** (via `genai` client)
- **Power BI** for dashboard creation
- **Jupyter Notebook** for prototyping
- `.env` file for environment variables and API keys

---

## 🧠 How It Works

1. Drop your PDF invoices into the `invoices/` folder.
2. Run `main.py` to extract and process them in batches.
3. Structured invoice data is saved in a DataFrame.
4. Use Power BI to load and visualize the `.csv` or connect to the database.

---

## 🔐 Notes

- This project requires a valid Gemini API key saved in a `.env` file:  
  `GENAI_API_KEY=your_api_key_here`
- To avoid API limits, invoices are processed in batches with a configurable delay.

---

## 👩‍💻 Author

**Kathia Borja**  
Industrial Management Student | Data Automation & Analytics Enthusiast  

---



