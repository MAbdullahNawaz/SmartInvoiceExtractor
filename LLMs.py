import google.generativeai as genai
import os
from PIL import Image
import sqlite3
import json
import re

# Set your API key
os.environ["GOOGLE_API_KEY"] = ""
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Load the image
image_path = r"C:\Users\Dell\Desktop\Image.jpg"
image = Image.open(image_path)

# ✅  model name
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

#  prompt


prompt = """
Given the image:

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
- Use **clear, human-readable key names** that match the context of the content (e.g., `"Name"`, `"Number"`, `"Email"`, `"IMEI"`, `"ItemName"`, etc.).  
- Normalize synonymous labels only when obvious (e.g., "Phone No." → `"Number"`).  
- **Do not fabricate or rename fields** beyond normalization.  
- Avoid any special characters in **key names** unless absolutely necessary in **values** (e.g., dashes in phone numbers like `"0303-6732310"`).  
- The output must be **pure JSON**:  
- Do **not** wrap it in code blocks (no ```json or ``` delimiters).  
- Do **not** include headings, explanations, labels, or formatting before or after.  
- Output must start and end with **only** the JSON object’s curly braces `{}`.


"""
#  Send image + prompt
response = model.generate_content([prompt, image])

# 🖨️ Output
response_text = response.text.strip()


print("🔍 Full Model Response:\n", response.text)

# Try to extract JSON only
match = re.search(r"\{.*\}", response.text, re.DOTALL)
cleaned_text = match.group(0).strip() if match else ""

if not cleaned_text:
    print("❌ No valid JSON found in the model response.")
    extracted_data = {}
else:
    try:
        extracted_data = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print("❌ Failed to parse JSON:", e)
        print("🔎 Cleaned Output:\n", cleaned_text)
        extracted_data = {}

con = sqlite3.connect("ocr_doc.db")
cursor = con.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    VendorName TEXT,
    InvoiceDate TEXT,
    TotalAmount REAL,
    InvoiceNumber INTEGER
)
""")

fields = ["VendorName", "InvoiceDate", "TotalAmount", "InvoiceNumber"]
data = {key: extracted_data.get(key, None) for key in fields}

cursor.execute("""
INSERT INTO invoices (VendorName, InvoiceDate, TotalAmount, InvoiceNumber)
VALUES (?, ?, ?, ?)
""", (data["VendorName"], data["InvoiceDate"], data["TotalAmount"], data["InvoiceNumber"]))

con.commit()
con.close()

print("✅ Data inserted successfully:", data)