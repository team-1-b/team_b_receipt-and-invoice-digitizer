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

