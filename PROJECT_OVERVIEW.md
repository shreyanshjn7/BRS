# Bank Statement Analyzer - Project Overview

## 🎯 What This App Does

This application helps you analyze bank statements and categorize transactions automatically to simplify income tax filing. Upload a PDF, CSV, or Excel file, and get:

1. **Automatic categorization** into 20+ categories (Fuel, Electricity, Groceries, Rent, etc.)
2. **Visual analysis** with charts and graphs
3. **Excel reports** ready for tax filing
4. **Editable categories** - fix any miscategorizations

## 📁 Project Structure

```
BRS/
├── backend/                    # Python Flask API
│   ├── app.py                 # Main backend logic
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Docker config for backend
│   └── uploads/              # Temporary upload folder (auto-created)
│
├── frontend/                  # React web interface
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styling
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Global styles
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── package.json          # Node.js dependencies
│   ├── Dockerfile           # Docker config for frontend
│   └── .env.example         # Environment variables template
│
├── sample_data/              # Test data
│   └── sample_statement.csv # Sample bank statement for testing
│
├── docker-compose.yml        # Run both services with Docker
├── .gitignore               # Git ignore rules
├── README.md                # Full documentation
├── SETUP_GUIDE.md           # Installation instructions
└── PROJECT_OVERVIEW.md      # This file
```

## 🔧 Technology Stack

### Backend (Python + Flask)
- **Flask**: Web framework for REST API
- **pandas**: Data processing and analysis
- **PyPDF2**: PDF text extraction
- **openpyxl**: Excel file generation
- **flask-cors**: Cross-origin resource sharing

### Frontend (React)
- **React**: UI framework
- **Axios**: HTTP client for API calls
- **Recharts**: Charts and visualizations
- **Lucide React**: Beautiful icons

## 🚀 Features Breakdown

### 1. File Upload & Parsing
- **Supported formats**: PDF, CSV, Excel (.xlsx, .xls)
- **Smart parsing**: Automatically detects date, description, amount columns
- **Flexible**: Works with different bank statement formats

### 2. Automatic Categorization
The app categorizes transactions using keyword matching:

| Category | Example Keywords |
|----------|-----------------|
| Salary/Income | salary, wages, credited |
| Fuel | petrol, diesel, indian oil, hp |
| Electricity | electricity, bescom, power bill |
| Groceries | bigbasket, dmart, supermarket |
| Rent | rent, lease, housing |
| Medical | hospital, pharmacy, doctor |
| ... and 15+ more categories |

### 3. Interactive Dashboard
- **Transaction Table**: View all transactions, filter by category
- **Inline Editing**: Click edit icon to change any category
- **Real-time Updates**: Analysis updates automatically

### 4. Visual Analysis
- **Summary Cards**: Total credit, debit, net balance
- **Pie Chart**: Expense distribution by category
- **Bar Charts**: Category-wise and monthly spending
- **Top Expenses**: Table of your 10 largest transactions

### 5. Excel Export
Generated Excel file contains 4 sheets:
1. **All Transactions**: Complete categorized list
2. **Category Summary**: Total amount per category
3. **Monthly Summary**: Month-wise breakdown
4. **Tax Relevant**: Filtered tax-deductible expenses

## 🎨 User Interface Flow

```
┌─────────────────────────────────────────────────┐
│         Upload Tab                              │
│  [Choose File] [Upload & Process]              │
│  Supported: PDF, CSV, Excel                     │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│         Transactions Tab (250 items)            │
│  Filter: [All Categories ▼]  [Export Excel]    │
│  ┌────────────────────────────────────────────┐ │
│  │ Date  Description  Amount  Type  Category  │ │
│  │ 01/01 Salary      75000   CR    Income     │ │
│  │ 05/01 Fuel        2500    DR    Fuel   [✏]│ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│         Analysis Tab                            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │ Credit  │ │  Debit  │ │   Net   │          │
│  │ ₹75,000 │ │ ₹50,000 │ │ ₹25,000 │          │
│  └─────────┘ └─────────┘ └─────────┘          │
│                                                 │
│  [Pie Chart]      [Bar Chart]                  │
│  Category Split   Monthly Trends               │
│                                                 │
│  [Export Complete Report]                      │
└─────────────────────────────────────────────────┘
```

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Check if API is running |
| `/api/upload` | POST | Upload and process file |
| `/api/categories` | GET | Get all category names |
| `/api/analyze` | POST | Generate analysis summary |
| `/api/export` | POST | Download Excel report |

## 💡 How to Use

### Quick Start
1. **Start Backend**: `cd backend && python app.py`
2. **Start Frontend**: `cd frontend && npm start`
3. **Open Browser**: Navigate to `http://localhost:3000`
4. **Upload File**: Use the provided sample CSV or your own statement
5. **Review**: Check transactions and edit categories if needed
6. **Export**: Download Excel report for tax filing

### Using Sample Data
```bash
# The sample file is in sample_data/sample_statement.csv
# It contains typical transactions:
# - Salary credits
# - Bill payments (electricity, phone)
# - Shopping (Amazon, Flipkart)
# - Food delivery (Zomato, Swiggy)
# - Transportation (Uber, Ola)
# - Insurance, medical, fuel, etc.
```

## 🎯 Tax Filing Use Cases

### For Salaried Individuals
- Track salary income (Form 16 verification)
- Identify deductible expenses:
  - Medical insurance premiums
  - Home loan EMI
  - Education fees
  - Life insurance premiums
- Calculate savings (80C, 80D sections)

### For Self-Employed/Business
- Separate business and personal expenses
- Track sales and purchase transactions
- Calculate business expenses:
  - Fuel for business travel
  - Office rent
  - Utility bills
  - Equipment purchases

### For GST Filing
- Identify all purchase invoices
- Track supplier payments
- Calculate input tax credit
- Monthly sales reconciliation

## 🔒 Privacy & Security

✅ **Local Processing**: All data processed on your machine  
✅ **No Cloud Storage**: Files automatically deleted after processing  
✅ **No External APIs**: No data sent to third parties  
✅ **Open Source**: Full transparency of code  

## 🚀 Deployment Options

### Option 1: Local Development
```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Terminal 2 - Frontend
cd frontend
npm install
npm start
```

### Option 2: Docker
```bash
docker-compose up --build
```

### Option 3: Production Deployment
- **Backend**: Deploy Flask on Heroku, AWS EB, DigitalOcean
- **Frontend**: Deploy React build on Vercel, Netlify, S3

## 🔧 Customization Guide

### Add New Categories

Edit `backend/app.py`:
```python
CATEGORIES = {
    'Your New Category': ['keyword1', 'keyword2', 'keyword3'],
    # ...
}
```

### Improve Categorization

Add more keywords to existing categories:
```python
'Fuel': [
    'petrol', 'diesel', 'fuel',
    'your_local_pump_name',  # Add this
    'ev charging',            # Add this
],
```

### Customize UI Colors

Edit `frontend/src/App.css`:
```css
.card-green {
  background: linear-gradient(135deg, #your-color 0%, #another-color 100%);
}
```

## 📊 Sample Output

### Console Output (Backend)
```
 * Running on http://127.0.0.1:5000
 * Processing file: sample_statement.csv
 * Extracted 24 transactions
 * Categorized into 12 categories
 * Analysis complete
```

### Excel Export Contains
```
Sheet 1: All Transactions
- Date, Description, Amount, Type, Category

Sheet 2: Category Summary
- Category Name, Total Amount, Transaction Count

Sheet 3: Monthly Summary
- Month, Total Amount

Sheet 4: Tax Relevant
- Filtered list of tax-deductible transactions
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Change port in app.py or stop conflicting service |
| Module not found | Run `pip install -r requirements.txt` |
| CORS errors | Check Flask CORS configuration |
| Can't connect to API | Ensure both backend and frontend are running |
| PDF not parsing | Try converting to CSV/Excel first |

## 📈 Future Enhancements

Potential features to add:
- [ ] Machine learning for better categorization
- [ ] Multi-account consolidation
- [ ] Budget tracking and alerts
- [ ] Recurring transaction detection
- [ ] Mobile app version
- [ ] OCR for scanned documents
- [ ] Multi-currency support
- [ ] User authentication
- [ ] Cloud sync (optional)

## 📝 License

MIT License - Free to use for personal or commercial purposes

## 🤝 Contributing

Feel free to:
- Add new categories
- Improve parsing logic
- Enhance UI/UX
- Fix bugs
- Add features

---

**Need Help?** Check README.md or SETUP_GUIDE.md for detailed instructions!
