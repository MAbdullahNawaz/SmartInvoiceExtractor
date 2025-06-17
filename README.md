<h1>InvoiceSnapAI 🧾 – Code-Centric Documentation</h1>

<p><strong>InvoiceSnapAI</strong> is a Python-based intelligent invoice processing system that extracts key structured data from invoice images using Google’s Gemini LLM, and stores it efficiently in a SQLite database. The system consists of two primary Python scripts:</p>

<ul>
    <li><strong>LLM_QT.py</strong> – The main PyQt5 GUI application for interactive use.</li>
    <li><strong>LLM.py</strong> – A standalone script for running extractions and database insertions directly.</li>
</ul>

<p>This README dives deep into the code’s flow, architecture, and logic.</p>

<hr>

<h2>🗂 Project File Breakdown</h2>

<h3>1. LLM_QT.py – Main GUI Application</h3>

<p><strong>Purpose:</strong></p>
<p>Provides a user-friendly graphical interface to upload invoice images, preview them, extract structured data using Gemini Pro, and optionally save the data to a local database.</p>

<p><strong>Key Components:</strong></p>
<ul>
    <li><code>init_db()</code>: Initializes the SQLite database and the invoices table.</li>
    <li><code>save_to_db(data)</code>: Saves extracted invoice data into the database.</li>
    <li><code>extract_json_from_image(image_path)</code>:
        <ul>
            <li>Loads the image.</li>
            <li>Sends the image along with a detailed extraction prompt to Google Gemini.</li>
            <li>Cleans the LLM’s response to isolate the JSON.</li>
            <li>Parses the JSON and returns the structured data.</li>
        </ul>
    </li>
    <li><code>InvoiceApp(QWidget)</code>: The main PyQt5 class that:
        <ul>
            <li>Displays a logo.</li>
            <li>Allows image selection using QFileDialog.</li>
            <li>Shows the selected image preview.</li>
            <li>Presents the extracted JSON in a text box.</li>
            <li>Asks the user whether to save the extracted data to the database.</li>
            <li>Handles success or failure notifications.</li>
        </ul>
    </li>
    <li><code>if __name__ == '__main__'</code>: Starts the PyQt5 GUI loop and initializes the database on launch.</li>
</ul>

<h3>2. LLM.py – Standalone Script</h3>

<p><strong>Purpose:</strong></p>
<p>Runs the complete extraction and database saving process directly from the terminal without using a GUI.</p>

<p><strong>Key Components:</strong></p>
<ul>
    <li>Loads the image directly from the file system.</li>
    <li>Sends the image with the detailed prompt to Google Gemini.</li>
    <li>Extracts JSON from the LLM’s response.</li>
    <li>Parses the JSON and saves it directly to the SQLite database.</li>
    <li>Logs extraction success or failure to the terminal.</li>
</ul>

<hr>

<h2>🔄 Detailed Code Workflow</h2>

<h3>🔧 Database Setup</h3>
<p>SQLite is used for lightweight, local storage.</p>
<p>The database table <code>invoices</code> contains:</p>
<pre>
id INTEGER PRIMARY KEY AUTOINCREMENT
VendorName TEXT
InvoiceDate TEXT
TotalAmount REAL
InvoiceNumber INTEGER
</pre>

<h3>🖼️ Image Selection</h3>
<ul>
    <li>In the GUI version, the user selects an invoice image using a file dialog.</li>
    <li>The selected image is displayed as a preview.</li>
</ul>

<h3>💡 LLM Extraction Process</h3>
<ul>
    <li>Both scripts use Google Gemini Pro (via <code>google.generativeai</code>) to process the image.</li>
    <li>A detailed, structured prompt guides the LLM to:
        <ul>
            <li>Extract the visible text from the image.</li>
            <li>Correct grammatical errors.</li>
            <li>Parse the text into a strict JSON schema containing:
                <ul>
                    <li>Vendor Name</li>
                    <li>Invoice Date</li>
                    <li>Total Amount</li>
                    <li>Invoice Number</li>
                </ul>
            </li>
            <li>Apply strict JSON formatting rules:
                <ul>
                    <li>No missing keys</li>
                    <li>No nested objects</li>
                    <li>Native types only</li>
                </ul>
            </li>
        </ul>
    </li>
</ul>

<h3>📦 JSON Parsing</h3>
<ul>
    <li>The raw response from Gemini is cleaned using regular expressions to isolate the JSON object.</li>
    <li>Python’s <code>json.loads()</code> is used to parse the JSON.</li>
</ul>

<h3>🗃️ Database Insertion</h3>
<ul>
    <li>The extracted data is inserted into the SQLite database using parameterized SQL queries for security.</li>
</ul>

<h3>🖥️ GUI Features</h3>
<ul>
    <li>The GUI shows:
        <ul>
            <li>A logo header.</li>
            <li>Text box displaying the extracted JSON.</li>
            <li>Image preview pane.</li>
            <li>Confirmation dialog asking whether to save the data.</li>
            <li>Status pop-ups for successful or failed operations.</li>
        </ul>
    </li>
</ul>
