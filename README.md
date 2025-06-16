InvoiceSnapAI 🧾 – Code-Centric Documentation
InvoiceSnapAI is a Python-based intelligent invoice processing system that extracts key structured data from invoice images using Google’s Gemini LLM, and stores it efficiently in a SQLite database. The system consists of two primary Python scripts:

LLM_QT.py – The main PyQt5 GUI application for interactive use.

LLM.py – A standalone script for running extractions and database insertions directly.

This README dives deep into the code’s flow, architecture, and logic.

🗂 Project File Breakdown
1. LLM_QT.py – Main GUI Application
Purpose:
Provides a user-friendly graphical interface to upload invoice images, preview them, extract structured data using Gemini Pro, and optionally save the data to a local database.

Key Components:

init_db(): Initializes the SQLite database and the invoices table.

save_to_db(data): Saves extracted invoice data into the database.

extract_json_from_image(image_path):

Loads the image.

Sends the image along with a detailed extraction prompt to Google Gemini.

Cleans the LLM’s response to isolate the JSON.

Parses the JSON and returns the structured data.

InvoiceApp(QWidget): The main PyQt5 class that:

Displays a logo.

Allows image selection using QFileDialog.

Shows the selected image preview.

Presents the extracted JSON in a text box.

Asks the user whether to save the extracted data to the database.

Handles success or failure notifications.

if __name__ == '__main__': Starts the PyQt5 GUI loop and initializes the database on launch.

2. LLM.py – Standalone Script
Purpose:
Runs the complete extraction and database saving process directly from the terminal without using a GUI.

Key Components:

Loads the image directly from the file system.

Sends the image with the detailed prompt to Google Gemini.

Extracts JSON from the LLM’s response.

Parses the JSON and saves it directly to the SQLite database.

Logs extraction success or failure to the terminal.

🔄 Detailed Code Workflow
🔧 Database Setup:
SQLite is used for lightweight, local storage.

The database table invoices contains:

sql
Copy
Edit
id INTEGER PRIMARY KEY AUTOINCREMENT
VendorName TEXT
InvoiceDate TEXT
TotalAmount REAL
InvoiceNumber INTEGER
🖼️ Image Selection:
In the GUI version, the user selects an invoice image using a file dialog.

The selected image is displayed as a preview.

💡 LLM Extraction Process:
Both scripts use Google Gemini Pro (via google.generativeai) to process the image.

A detailed, structured prompt guides the LLM to:

Extract the visible text from the image.

Correct grammatical errors.

Parse the text into a strict JSON schema containing:

Vendor Name

Invoice Date

Total Amount

Invoice Number

Apply strict JSON formatting rules (no missing keys, no nested objects, native types).

📦 JSON Parsing:
The raw response from Gemini is cleaned using regular expressions to isolate the JSON object.

Python’s json.loads() is used to parse the JSON.

🗃️ Database Insertion:
The extracted data is inserted into the SQLite database using parameterized SQL queries for security.

🖥️ GUI Features:
The GUI shows:

A logo header.

Text box displaying the extracted JSON.

Image preview pane.

Confirmation dialog asking whether to save the data.

Status pop-ups for successful or failed operations.
