import sys
import os
import json
import re
import sqlite3
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QTextEdit, QFileDialog,
    QMessageBox, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
import google.generativeai as genai

# ---------- GOOGLE GEMINI API CONFIGURATION ----------
os.environ["GOOGLE_API_KEY"] = ""
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect("")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            VendorName TEXT,
            InvoiceDate TEXT,
            TotalAmount REAL,
            InvoiceNumber INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(data):
    conn = sqlite3.connect("")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO invoices (VendorName, InvoiceDate, TotalAmount, InvoiceNumber)
        VALUES (?, ?, ?, ?)
    """, (
        data.get("VendorName"),
        data.get("InvoiceDate"),
        data.get("TotalAmount"),
        data.get("InvoiceNumber")
    ))
    conn.commit()
    conn.close()

# ---------- IMAGE TO JSON EXTRACTION LOGIC ----------
def extract_json_from_image(image_path):
    image = Image.open(image_path)
    prompt = """
You are given an image containing text.    
You are given an image containing text.    
1. **Extract** all clearly visible and confidently readable text from the image.  
2. **Correct** any grammar or spelling errors in the extracted text.  
3. **Analyze** the corrected text and convert it into a **valid, flat JSON object**.  
4. Extract the Vendor name. Use your intelligence to identify other possible terms or labels commonly used to refer to a vendor (e.g., "Supplier", "Merchant", "Shop                      Name", "Store", etc.), and match accordingly.
5. Extract the date from the image. Identify commonly used synonyms or formats such as "Date", "Invoice Date", "Billing Date", or any standard date formats (e.g., DD/MM/YYYY, MM-DD-YYYY, etc.).
6. Extract the "Total Bill" or "Total Amount". Recognize alternate phrases like "Amount Due", "Total Due", "Total Payable", "Bill Total", "Grand Total", or simply "Total".
7. Every invoice contains an Invoice Number. Analyze the image to identify the Invoice Number, which might appear under other names like "Invoice No", "Receipt No", "Bill No", "Order No", "Ref No", or similar terms indicating a unique identifying number for the document.        
8. Only extract and include the following 4 fields in the final JSON: "VendorName", "InvoiceDate", "TotalAmount", and "InvoiceNumber". If no value is matched or extracted for any of these fields, include the key with a value of null. Do not extract or include any other fields under any circumstance.

 ⚠️ The JSON must follow these strict rules:  
- Only include information that **explicitly exists in the image**. Do **not infer or guess** missing data.  
- Use **double quotes** only for keys and string values.  
- Use **native types** for numbers (integers or floats) and booleans — **do not wrap them in quotes**.  
- Do **not include null, undefined, or placeholder values**. If a value is missing, simply **omit the key entirely**.  
- Keep the structure **flat** — do **not nest objects** unless absolutely necessary based on the content's meaning.  
- Use **clear, human-readable key names** that match the context of the content (e.g., "Name", "Number", "Email", "IMEI", "ItemName", etc.).  
- Normalize synonymous labels only when obvious (e.g., "Phone No." → "Number").  
- **Do not fabricate or rename fields** beyond normalization.  
- Avoid any special characters in **key names** unless absolutely necessary in **values** (e.g., dashes in phone numbers like "0303-6732310").  
- The output must be **pure JSON**:  
- Do **not** wrap it in code blocks (no 
json or
 delimiters).  
- Do **not** include headings, explanations, labels, or formatting before or after.  
- Output must start and end with **only** the JSON object’s curly braces {}.
    """
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content([prompt, image])
    response_text = response.text.strip()

    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    cleaned_text = match.group(0).strip() if match else ""

    if not cleaned_text:
        return {}, "No valid JSON found."

    try:
        extracted_data = json.loads(cleaned_text)
        return extracted_data, "Success"
    except json.JSONDecodeError as e:
        return {}, f"Failed to parse JSON: {e}"

# ---------- MAIN APPLICATION ----------
class InvoiceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("From Scanned to Structured in Seconds")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Logo display
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setFixedHeight(100)
        self.set_logo("C:/Users/Dell/Desktop/LOGO.jpeg.jpeg")  # ✅ <---- Set your logo path here

        # Output box for JSON
        self.text_output = QTextEdit()
        self.text_output.setPlaceholderText("Your Invoice Data Snapshot Awaits Here...")

        # Section label
        self.section_label = QLabel("📄 Upload Your Invoice Image for Smart Extraction")
        self.section_label.setFont(QFont("Segoe UI", 10))
        self.section_label.setAlignment(Qt.AlignLeft)

        # Button to select image
        self.btn = QPushButton("Select Invoice Image")
        self.btn.clicked.connect(self.select_image)

        # Image preview area (newly added)
        self.image_preview_label = QLabel("Image Preview")
        self.image_preview_label.setAlignment(Qt.AlignCenter)
        self.image_preview_label.setFixedHeight(300)

        # Layout setup
        main_layout.addWidget(self.logo_label)
        main_layout.addWidget(self.text_output)
        main_layout.addWidget(self.section_label)
        main_layout.addWidget(self.btn)
        main_layout.addWidget(self.image_preview_label)

        self.setLayout(main_layout)

    def set_logo(self, path):
        if os.path.exists(path):
            pixmap = QPixmap(path)
            # Stretch logo to full width of the window while keeping aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.width(),  # Width: stretch to the window's width
                120,  # Height: fixed or adjustable (you can tune this value)
                Qt.KeepAspectRatioByExpanding,  # Expand and crop if needed
                Qt.SmoothTransformation  # Smooth scaling
            )
            self.logo_label.setPixmap(scaled_pixmap)
            self.logo_label.setFixedHeight(120)  # Adjust height accordingly
        else:
            self.logo_label.setText("Company Logo Here")

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            # Display selected image in the preview box
            pixmap = QPixmap(file_path)
            self.image_preview_label.setPixmap(pixmap.scaledToHeight(300))

            data, status = extract_json_from_image(file_path)
            if status == "Success":
                self.text_output.setText(json.dumps(data, indent=2))

                reply = QMessageBox.question(
                    self,
                    'Save Extracted Data?',
                    "Data extracted successfully.\nDo you want to save it to the database?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )

                if reply == QMessageBox.Yes:
                    save_to_db(data)
                    QMessageBox.information(self, "Saved", "Data has been saved successfully!")
                else:
                    QMessageBox.information(self, "Not Saved", "Data was not saved to the database.")

            else:
                self.text_output.setText(status)
                QMessageBox.warning(self, "Error", status)


# ---------- RUN APPLICATION ----------
if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    window = InvoiceApp()
    window.show()
    sys.exit(app.exec_())
