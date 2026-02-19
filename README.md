# Receipt-and-Invoice-Digitizer

### Description:

**MyDigiBill** is an automated receipt and invoice digitization system that inputs images/document through multiple formats (jpg, png, pdf), preprocesses them for optimal quality, and uses OCR technology (Tesseract) to extract text. An NLP-based extraction + regex engine then intelligently identifies and structures key fields like vendor details, line items, amounts, dates, and taxes into a standardized database format. The system validates extracted data against business rules, stores it in a searchable database with original image references, and provides API integration with popular accounting/ERP systems along with a user-friendly dashboard for review, search, analytics, and export capabilities—ultimately eliminating manual data entry, reducing errors, and enabling real-time financial insights.

### Prerequisites:

Before running the application, ensure you have the following installed:

- **Python**: Version 3.8 or higher
- **pip**: Python package manager
- **Git**: For cloning the repository

### Steps to Run the App (on your system):

#### 1. Clone the Repository

```bash
git clone https://github.com/Mayank2177/team_b_receipt-and-invoice-digitizer.git
```

#### 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the Application
Run the command:
```bash
streamlit run app.py
```
The application will be available at `http://localhost:5000`

By default Streamlit serves at http://localhost:8501. To use a specific port (e.g. 8080):
```bash
streamlit run app.py --server.port 8080
```

If you want to run headless (useful on servers):
```bash
streamlit run app.py --server.headless true --server.port 8501
```

### Troubleshooting:

| Issue | Solution |
|-------|----------|
| Tesseract not found | Ensure Tesseract is installed and path is correctly configured |
| OCR accuracy issues | Use high-quality images (300+ DPI) and ensure good lighting |
| Database errors | Check database connection string in .env file |
| Spacy "en_core_web_sm" not found | Run `python -m spacy download en_core_web_sm` again |


### License:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Version**: 1.0.0
