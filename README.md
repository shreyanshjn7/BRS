# Bank Statement Analyzer

A comprehensive web application to analyze bank statements, automatically categorize transactions, and generate reports for income tax filing.

## Features

✅ **Multi-Format Support**: Upload bank statements in PDF, CSV, or Excel (XLSX/XLS) formats  
✅ **Smart Categorization**: Automatically categorizes transactions into 20+ categories:
- Income: Salary/Income, Sales
- Expenses: Fuel, Electricity, Water, Groceries, Rent, EMI/Loan, Insurance, Medical, Education, Entertainment, Food & Dining, Shopping, Transportation, Telephone/Internet
- Financial: Purchases, Investments, Taxes, Bank Charges, Withdrawals, Transfers
- Other: Miscellaneous transactions

✅ **Interactive Dashboard**: 
- View all transactions in a sortable table
- Filter by category
- Edit categories manually if needed
- Visual charts and graphs for spending analysis

✅ **Analysis & Insights**:
- Category-wise spending breakdown
- Monthly spending trends
- Credit vs Debit summary
- Top 10 expenses
- Pie charts and bar charts for visualization

✅ **Export Functionality**: 
- Export to Excel with multiple sheets
- All transactions with categories
- Category summary
- Monthly summary
- Tax-relevant transactions (separate sheet)

## Technology Stack

**Backend:**
- Flask (Python web framework)
- pandas (Data processing)
- PyPDF2 (PDF parsing)
- openpyxl (Excel generation)

**Frontend:**
- React.js
- Recharts (Charts and visualizations)
- Lucide React (Icons)
- Axios (API calls)

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend API will start at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Create a `.env` file (optional):
```bash
cp .env.example .env
```

4. Start the React development server:
```bash
npm start
```

The frontend will start at `http://localhost:3000`

## Usage Guide

### Step 1: Upload Bank Statement
1. Open the app in your browser (`http://localhost:3000`)
2. Click on the "Choose File" button
3. Select your bank statement (PDF, CSV, or Excel)
4. Click "Upload & Process"

### Step 2: Review Transactions
1. Navigate to the "Transactions" tab
2. Review all extracted transactions
3. Filter by category if needed
4. Click the edit icon to manually change any category
5. Categories are automatically saved and analysis updates in real-time

### Step 3: View Analysis
1. Navigate to the "Analysis" tab
2. View comprehensive insights:
   - Total Credit, Debit, and Net Balance
   - Pie chart showing expense distribution
   - Bar chart for category-wise spending
   - Monthly spending trends
   - Top 10 expenses table

### Step 4: Export Report
1. Click "Export to Excel" button
2. The exported file contains:
   - **All Transactions**: Complete list with categories
   - **Category Summary**: Total amount per category
   - **Monthly Summary**: Month-wise breakdown
   - **Tax Relevant**: Filtered view of tax-relevant categories

## Sample Data

A sample CSV file is provided in `sample_data/sample_statement.csv` for testing purposes. This file contains typical transactions including:
- Salary credits
- Fuel expenses
- Grocery shopping
- Bill payments
- Rent
- Insurance premiums
- And more...

## Customization

### Adding New Categories

Edit `backend/app.py` and modify the `CATEGORIES` dictionary:

```python
CATEGORIES = {
    'Your Category Name': ['keyword1', 'keyword2', 'keyword3'],
    # Add more categories...
}
```

### Adjusting Category Keywords

Add more keywords to existing categories to improve auto-categorization accuracy:

```python
'Fuel': ['petrol', 'diesel', 'fuel', 'gas station', 'your_local_pump_name'],
```

## File Formats

### CSV Format
Your CSV should have columns for:
- Date (any common format: DD/MM/YYYY, DD-MM-YYYY, etc.)
- Description/Narration
- Amount
- Type (Credit/Debit) - optional

### PDF Format
- The app attempts to extract text from PDF bank statements
- Works best with text-based PDFs (not scanned images)
- Supports most common bank statement formats

### Excel Format
- Both .xlsx and .xls formats supported
- Automatically converts to CSV for processing
- Same column requirements as CSV

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check API status |
| `/api/upload` | POST | Upload and process bank statement |
| `/api/categories` | GET | Get all available categories |
| `/api/analyze` | POST | Analyze transactions and generate summary |
| `/api/export` | POST | Export categorized data to Excel |

## Troubleshooting

### Backend Issues

**Error: Module not found**
```bash
pip install -r requirements.txt
```

**Port 5000 already in use**
- Change the port in `app.py`: `app.run(port=5001)`
- Update frontend `.env`: `REACT_APP_API_URL=http://localhost:5001/api`

### Frontend Issues

**Error: Cannot connect to backend**
- Ensure backend is running on port 5000
- Check CORS settings in `app.py`
- Verify API URL in `.env` file

**Blank page or errors**
```bash
rm -rf node_modules package-lock.json
npm install
npm start
```

## Tax Filing Use Cases

This tool helps with:

1. **Income Tax Returns (ITR)**
   - Identify all salary/income deposits
   - Track deductible expenses (medical, insurance, education)
   - Calculate investment amounts (SIP, mutual funds)

2. **Business Expenses**
   - Separate business purchases from personal expenses
   - Track fuel expenses for travel claims
   - Calculate electricity and rent for home office deductions

3. **GST Returns**
   - Identify sales transactions
   - Track purchase invoices
   - Calculate input tax credit eligible expenses

4. **Audit Preparation**
   - Organized transaction records
   - Category-wise summaries
   - Monthly spending patterns

## Privacy & Security

- All processing happens locally on your machine
- No data is sent to external servers
- Uploaded files are automatically deleted after processing
- No transaction data is stored permanently

## Future Enhancements

- [ ] Machine Learning for improved categorization
- [ ] Multi-account statement consolidation
- [ ] Budget tracking and alerts
- [ ] Recurring transaction detection
- [ ] PDF generation for reports
- [ ] Mobile app version
- [ ] OCR support for scanned PDFs
- [ ] Bank-specific parsers
- [ ] Multi-user support with authentication

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Improve categorization logic
- Add support for more bank formats

## License

MIT License - Feel free to use this for personal or commercial purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review sample data format
3. Ensure all dependencies are installed
4. Check that both backend and frontend are running

## Version History

**v1.0.0** (Current)
- Initial release
- Multi-format support (PDF, CSV, Excel)
- 20+ transaction categories
- Interactive dashboard
- Analysis charts
- Excel export functionality

---

Built with ❤️ for simplifying tax filing and financial management
