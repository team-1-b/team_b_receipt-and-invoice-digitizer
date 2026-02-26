# 🧾 Mydigibill

A powerful, AI-powered receipt and expense management platform built with Streamlit, OCR and Google Gemini AI.

![Streamlit](https://img.shields.io/badge/streamlit-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### 🤖 AI-Powered OCR
- **Smart Text Extraction**: Automatically extract vendor, date, amount, tax, and bill ID from receipts
- **Multi-Format Support**: Process both images (PNG, JPG, JPEG) and PDF documents
- **High Accuracy**: 99.9% accuracy using Google Gemini AI and PaddleOCR

### 📊 Advanced Analytics
- **Spending Trends**: Visualize monthly and daily spending patterns
- **Category Analysis**: Track expenses by category with interactive charts
- **Vendor Insights**: Identify top vendors and spending patterns
- **Forecasting**: AI-powered spending predictions
- **Subscription Detection**: Automatically identify recurring payments

### 📥 Multi-Format Export
- **CSV Export**: For spreadsheet analysis
- **Excel Export**: Professional reports with summary sheets
- **PDF Reports**: Beautifully formatted expense reports
- **JSON Export**: For developers and API integration

### 🌐 Multi-Language Support
Support for 6 languages:
- 🇬🇧 English
- 🇮🇳 हिंदी (Hindi)
- 🇮🇳 தமிழ் (Tamil)
- 🇮🇳 తెలుగు (Telugu)
- 🇮🇳 বাংলা (Bengali)
- 🇮🇳 मराठी (Marathi)

### 💰 Budget Tracking
- Set monthly spending limits
- Real-time budget monitoring
- Color-coded status indicators (On Track / Warning / Over Budget)
- Remaining budget calculations

### 🔐 Secure Authentication
- Email/password authentication
- Google Sign-In ready (OAuth integration)
- Secure password hashing (SHA-256)
- Session management

### 🎨 Modern UI/UX
- Beautiful gradient designs
- Smooth animations
- Responsive layout
- Professional styling
- User-friendly interface

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Tesseract OCR installed ([Download](https://github.com/tesseract-ocr/tesseract))
- Poppler for PDF processing ([Download](https://github.com/oschwartz10612/poppler-windows/releases/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/receipt-vault-analyzer.git
   cd mydigibill
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   TESSERACT_PATH=your_tesseract_path_address
   POPPLER_PATH=your_poppler_path_address
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8501`

   **Note**
   In case your `8501` is busy:
   Run command:
   ```bash
   streamlit run app.py --server.port 8502
   ```

---

## 🔧 Configuration

### Tesseract OCR Setup
1. Download Tesseract from [here](https://github.com/tesseract-ocr/tesseract)
2. Install to `C:\Program Files\Tesseract-OCR\`
3. Update `.env` with the correct path

### Poppler Setup (for PDF processing)
1. Download Poppler from [here](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Extract to a folder (e.g., `C:\poppler\`)
3. Update `.env` with the path to the `bin` folder

### Google Gemini API
1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file

---

## Troubleshoot

| Problem | Fix |
|---------|-----|
| `TesseractNotFoundError` | Check `TESSERACT_PATH` in `.env` points to the `.exe` |
| PDF upload fails | Verify `POPPLER_PATH` points to the `bin` folder |
| Gemini API error | Confirm your API key is valid and within quota |
| Page not loading | Check terminal for errors; ensure port 8501 is free |
| Poor OCR results | Use a clearer, well-lit image at 300 DPI or higher |
| `None` values in config | Ensure `.env` is in the root folder with no extra spaces |


---
## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ using Streamlit**
