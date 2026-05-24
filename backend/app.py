from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import PyPDF2
import re
import io
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'xlsx', 'xls'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Transaction categories with keywords
CATEGORIES = {
    'Salary/Income': ['salary', 'income', 'wages', 'payment received', 'credited', 'deposit'],
    'Fuel': ['petrol', 'diesel', 'fuel', 'gas station', 'bharat petroleum', 'indian oil', 'hp', 'shell'],
    'Electricity': ['electricity', 'power', 'bescom', 'msedcl', 'tneb', 'discom', 'electric bill'],
    'Water': ['water', 'bwssb', 'water bill', 'municipal water'],
    'Groceries': ['grocery', 'supermarket', 'bigbasket', 'dmart', 'reliance fresh', 'more', 'store'],
    'Rent': ['rent', 'lease', 'housing rent'],
    'EMI/Loan': ['emi', 'loan', 'home loan', 'car loan', 'personal loan', 'credit card'],
    'Insurance': ['insurance', 'premium', 'lic', 'policy'],
    'Medical': ['hospital', 'medical', 'pharmacy', 'doctor', 'clinic', 'health'],
    'Education': ['school', 'college', 'university', 'tuition', 'education', 'course fee'],
    'Entertainment': ['movie', 'netflix', 'amazon prime', 'spotify', 'entertainment'],
    'Food & Dining': ['restaurant', 'zomato', 'swiggy', 'cafe', 'food', 'dining', 'hotel'],
    'Shopping': ['amazon', 'flipkart', 'myntra', 'shopping', 'mall', 'online purchase'],
    'Transportation': ['uber', 'ola', 'taxi', 'metro', 'bus', 'auto', 'transport'],
    'Telephone/Internet': ['airtel', 'jio', 'vodafone', 'bsnl', 'mobile', 'broadband', 'internet'],
    'Sales': ['sales', 'revenue', 'customer payment', 'invoice payment'],
    'Purchase': ['purchase', 'supplier payment', 'vendor payment', 'procurement'],
    'Investments': ['mutual fund', 'sip', 'stock', 'shares', 'investment', 'trading'],
    'Taxes': ['tax', 'tds', 'gst', 'income tax', 'advance tax'],
    'Bank Charges': ['bank charge', 'service charge', 'atm charge', 'annual fee'],
    'Withdrawal': ['atm withdrawal', 'cash withdrawal', 'withdrawal'],
    'Transfer': ['transfer', 'neft', 'imps', 'rtgs', 'upi'],
    'Other': []
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def parse_bank_statement_text(text):
    """Parse bank statement text and extract transactions"""
    transactions = []
    
    # Common patterns for bank statements
    # Pattern: Date Amount Description
    patterns = [
        r'(\d{2}[/-]\d{2}[/-]\d{4}|\d{2}[/-]\d{2}[/-]\d{2})\s+([^\s]+.*?)\s+([\d,]+\.?\d*)\s*(CR|DR|Cr|Dr)?',
        r'(\d{2}[/-]\w{3}[/-]\d{4})\s+([^\s]+.*?)\s+([\d,]+\.?\d*)\s*(CR|DR)?',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.MULTILINE)
        for match in matches:
            try:
                date = match.group(1)
                description = match.group(2).strip()
                amount = float(match.group(3).replace(',', ''))
                trans_type = match.group(4) if len(match.groups()) > 3 else ''
                
                transactions.append({
                    'date': date,
                    'description': description,
                    'amount': amount,
                    'type': 'Credit' if 'CR' in trans_type.upper() else 'Debit',
                    'category': 'Uncategorized'
                })
            except:
                continue
    
    return transactions

def parse_csv_statement(file_path):
    """Parse CSV bank statement"""
    try:
        df = pd.read_csv(file_path)
        
        # Try to identify columns (flexible matching)
        date_col = None
        desc_col = None
        amount_col = None
        type_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'date' in col_lower:
                date_col = col
            elif 'desc' in col_lower or 'narration' in col_lower or 'particular' in col_lower:
                desc_col = col
            elif 'amount' in col_lower or 'debit' in col_lower or 'credit' in col_lower:
                if amount_col is None:
                    amount_col = col
            elif 'type' in col_lower:
                type_col = col
        
        if not all([date_col, desc_col, amount_col]):
            # If columns not found, assume first 3-4 columns
            cols = df.columns.tolist()
            date_col = cols[0] if len(cols) > 0 else None
            desc_col = cols[1] if len(cols) > 1 else None
            amount_col = cols[2] if len(cols) > 2 else None
        
        transactions = []
        for _, row in df.iterrows():
            try:
                amount = float(str(row[amount_col]).replace(',', '').replace('₹', '').strip()) if pd.notna(row[amount_col]) else 0
                transactions.append({
                    'date': str(row[date_col]),
                    'description': str(row[desc_col]),
                    'amount': abs(amount),
                    'type': str(row[type_col]) if type_col and pd.notna(row[type_col]) else ('Credit' if amount > 0 else 'Debit'),
                    'category': 'Uncategorized'
                })
            except:
                continue
        
        return transactions
    except Exception as e:
        raise Exception(f"Error parsing CSV: {str(e)}")

def categorize_transaction(description):
    """Categorize transaction based on description"""
    description_lower = description.lower()
    
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in description_lower:
                return category
    
    return 'Other'

def categorize_transactions(transactions):
    """Apply categorization to all transactions"""
    for transaction in transactions:
        transaction['category'] = categorize_transaction(transaction['description'])
    return transactions

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Bank Statement Analyzer API is running'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and process bank statement"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PDF, CSV, XLSX, XLS'}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process file based on extension
        transactions = []
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext == 'pdf':
            with open(file_path, 'rb') as f:
                text = extract_text_from_pdf(f)
                transactions = parse_bank_statement_text(text)
        elif file_ext == 'csv':
            transactions = parse_csv_statement(file_path)
        elif file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file_path)
            df.to_csv(file_path.replace(file_ext, 'csv'), index=False)
            transactions = parse_csv_statement(file_path.replace(file_ext, 'csv'))
        
        # Categorize transactions
        transactions = categorize_transactions(transactions)
        
        # Clean up uploaded file
        os.remove(file_path)
        if os.path.exists(file_path.replace(file_ext, 'csv')):
            os.remove(file_path.replace(file_ext, 'csv'))
        
        return jsonify({
            'success': True,
            'transactions': transactions,
            'count': len(transactions)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available categories"""
    return jsonify({'categories': list(CATEGORIES.keys())})

@app.route('/api/analyze', methods=['POST'])
def analyze_transactions():
    """Analyze transactions and generate summary"""
    try:
        data = request.json
        transactions = data.get('transactions', [])
        
        if not transactions:
            return jsonify({'error': 'No transactions provided'}), 400
        
        df = pd.DataFrame(transactions)
        
        # Category-wise summary
        category_summary = df.groupby('category').agg({
            'amount': 'sum',
            'date': 'count'
        }).reset_index()
        category_summary.columns = ['category', 'total_amount', 'transaction_count']
        category_summary = category_summary.sort_values('total_amount', ascending=False)
        
        # Type-wise summary (Credit vs Debit)
        type_summary = df.groupby('type').agg({
            'amount': 'sum'
        }).reset_index()
        
        # Monthly summary
        df['date'] = pd.to_datetime(df['date'], errors='coerce', infer_datetime_format=True)
        df['month'] = df['date'].dt.to_period('M').astype(str)
        monthly_summary = df.groupby('month').agg({
            'amount': 'sum',
            'date': 'count'
        }).reset_index()
        monthly_summary.columns = ['month', 'total_amount', 'transaction_count']
        
        # Top expenses
        top_expenses = df.nlargest(10, 'amount')[['date', 'description', 'amount', 'category']].to_dict('records')
        
        return jsonify({
            'category_summary': category_summary.to_dict('records'),
            'type_summary': type_summary.to_dict('records'),
            'monthly_summary': monthly_summary.to_dict('records'),
            'top_expenses': top_expenses,
            'total_credit': float(df[df['type'] == 'Credit']['amount'].sum()),
            'total_debit': float(df[df['type'] == 'Debit']['amount'].sum()),
            'net_balance': float(df[df['type'] == 'Credit']['amount'].sum() - df[df['type'] == 'Debit']['amount'].sum())
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_report():
    """Export categorized transactions to Excel"""
    try:
        data = request.json
        transactions = data.get('transactions', [])
        
        if not transactions:
            return jsonify({'error': 'No transactions provided'}), 400
        
        df = pd.DataFrame(transactions)
        
        # Create Excel file with multiple sheets
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # All transactions
            df.to_excel(writer, sheet_name='All Transactions', index=False)
            
            # Category summary
            category_summary = df.groupby('category').agg({
                'amount': 'sum',
                'date': 'count'
            }).reset_index()
            category_summary.columns = ['Category', 'Total Amount', 'Transaction Count']
            category_summary.to_excel(writer, sheet_name='Category Summary', index=False)
            
            # Monthly summary
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['month'] = df['date'].dt.to_period('M').astype(str)
            monthly_summary = df.groupby('month').agg({
                'amount': 'sum'
            }).reset_index()
            monthly_summary.columns = ['Month', 'Total Amount']
            monthly_summary.to_excel(writer, sheet_name='Monthly Summary', index=False)
            
            # Tax-relevant categories
            tax_categories = ['Salary/Income', 'Rent', 'Medical', 'Education', 'Insurance', 'Investments', 'Taxes']
            tax_df = df[df['category'].isin(tax_categories)]
            if not tax_df.empty:
                tax_summary = tax_df.groupby('category').agg({
                    'amount': 'sum'
                }).reset_index()
                tax_summary.columns = ['Category', 'Total Amount']
                tax_summary.to_excel(writer, sheet_name='Tax Relevant', index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'bank_statement_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-category', methods=['POST'])
def update_category():
    """Update category for a transaction"""
    try:
        data = request.json
        # This is handled on frontend, just return success
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
