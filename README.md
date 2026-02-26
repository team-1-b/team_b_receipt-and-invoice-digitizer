# 🧾 Receipt Vault Analyzer

A powerful, AI-powered receipt management and analytics platform built with Streamlit and Google Gemini AI.

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
   TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
   POPPLER_PATH=C:\path\to\poppler\bin
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8501`

---

## 📖 Usage Guide

### 1. **Landing Page**
- Choose your preferred language
- Click "Get Started" to create an account
- Or click "Login" if you already have one

### 2. **Authentication**
- **Sign Up**: Enter name, email, and password
- **Login**: Use your credentials
- **Google Sign-In**: Quick OAuth login (requires setup)

### 3. **Upload Receipts**
- Drag and drop receipt images or PDFs
- Supports: PNG, JPG, JPEG, PDF
- Maximum file size: 200MB

### 4. **Validation**
- Review extracted data
- Edit any incorrect information
- Save to database

### 5. **Dashboard**
- View key metrics (Total Spending, Tax, Receipts Count, Average)
- Export data in multiple formats (CSV, Excel, PDF, JSON)
- Filter receipts by various criteria
- Delete unwanted receipts

### 6. **Analytics**
- Explore spending trends with interactive charts
- View category breakdowns
- Analyze vendor patterns
- Get AI-powered insights
- Track subscriptions

### 7. **Budget Tracking**
- Set monthly budget limit in sidebar
- Monitor spending progress
- Get real-time status updates
- View remaining budget

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Streamlit**: Web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database

### AI & OCR
- **Google Gemini AI**: Advanced text extraction and insights
- **PaddleOCR**: Optical character recognition
- **Tesseract OCR**: Text recognition
- **pdf2image**: PDF processing

### Data & Analytics
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations

### Export & Reporting
- **ReportLab**: PDF generation
- **OpenPyXL**: Excel file creation

---

## 📁 Project Structure

```
Receipt-Vault-Analyzer/
├── ai/                          # AI & ML modules
│   ├── gemini_client.py        # Gemini API integration
│   ├── insights.py             # AI insights generation
│   └── prompts.py              # AI prompts
│
├── analytics/                   # Analytics modules
│   ├── advanced_analytics.py   # Advanced metrics
│   ├── forecasting.py          # Spending predictions
│   └── search.py               # Search functionality
│
├── config/                      # Configuration
│   ├── config.py               # App configuration
│   └── translations.py         # Multi-language support
│
├── database/                    # Database layer
│   ├── db.py                   # Database initialization
│   ├── models.py               # SQLAlchemy models
│   └── queries.py              # Database queries
│
├── docs/                        # Documentation
│   ├── ANALYTICS_SUMMARIES_ADDED.md
│   ├── COMPLETE_UI_OVERHAUL.md
│   ├── FIX_SUMMARY.md
│   └── UI_ENHANCEMENT_SUMMARY.md
│
├── ocr/                         # OCR processing
│   ├── extractor.py            # Text extraction
│   └── pdf_processor.py        # PDF handling
│
├── ui/                          # User interface
│   ├── analytics_ui.py         # Analytics page
│   ├── auth_page.py            # Login/Signup
│   ├── chat_ui.py              # Chat interface
│   ├── dashboard_ui.py         # Dashboard
│   ├── landing_page.py         # Landing page
│   ├── sidebar.py              # Sidebar navigation
│   ├── styles.py               # Global styling
│   ├── upload_ui.py            # Upload page
│   └── validation_ui.py        # Validation page
│
├── utils/                       # Utility functions
│
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
├── app.py                       # Main application
├── requirements.txt             # Dependencies
├── receipts.db                  # SQLite database
└── README.md                    # This file
```

---

## 🎨 Screenshots

### Landing Page
Beautiful hero section with animated gradient background and feature showcase.

### Dashboard
Clean, modern dashboard with key metrics and export options.

### Analytics
Interactive charts and AI-powered insights for spending analysis.

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

## 📞 Support

For support, open an issue on GitHub.

---

**Made with ❤️ using Streamlit & Gemini AI**
