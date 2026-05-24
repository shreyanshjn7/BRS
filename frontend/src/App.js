import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileText, TrendingUp, Download, Edit2, Save, X } from 'lucide-react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF6B9D', '#C084FC', '#FB923C'];

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [transactions, setTransactions] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [activeTab, setActiveTab] = useState('upload');
  const [editingIndex, setEditingIndex] = useState(null);
  const [categories, setCategories] = useState([]);
  const [filterCategory, setFilterCategory] = useState('All');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setTransactions(response.data.transactions);
      setActiveTab('transactions');
      
      // Get categories
      const catResponse = await axios.get(`${API_URL}/categories`);
      setCategories(catResponse.data.categories);
      
      // Analyze transactions
      await analyzeTransactions(response.data.transactions);
      
      alert(`Successfully processed ${response.data.count} transactions!`);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error processing file: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const analyzeTransactions = async (txns) => {
    try {
      const response = await axios.post(`${API_URL}/analyze`, {
        transactions: txns || transactions,
      });
      setAnalysis(response.data);
    } catch (error) {
      console.error('Error analyzing transactions:', error);
    }
  };

  const handleCategoryChange = (index, newCategory) => {
    const updatedTransactions = [...transactions];
    updatedTransactions[index].category = newCategory;
    setTransactions(updatedTransactions);
    setEditingIndex(null);
    analyzeTransactions(updatedTransactions);
  };

  const handleExport = async () => {
    try {
      const response = await axios.post(`${API_URL}/export`, {
        transactions,
      }, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `bank_statement_analysis_${new Date().getTime()}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error exporting:', error);
      alert('Error exporting data');
    }
  };

  const filteredTransactions = filterCategory === 'All' 
    ? transactions 
    : transactions.filter(t => t.category === filterCategory);

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <FileText size={32} />
          <h1>Bank Statement Analyzer</h1>
          <p>Categorize transactions for easy tax filing</p>
        </div>
      </header>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          <Upload size={18} /> Upload
        </button>
        <button 
          className={`tab ${activeTab === 'transactions' ? 'active' : ''}`}
          onClick={() => setActiveTab('transactions')}
          disabled={transactions.length === 0}
        >
          <FileText size={18} /> Transactions ({transactions.length})
        </button>
        <button 
          className={`tab ${activeTab === 'analysis' ? 'active' : ''}`}
          onClick={() => setActiveTab('analysis')}
          disabled={!analysis}
        >
          <TrendingUp size={18} /> Analysis
        </button>
      </div>

      <div className="content">
        {activeTab === 'upload' && (
          <div className="upload-section">
            <div className="upload-card">
              <Upload size={48} className="upload-icon" />
              <h2>Upload Bank Statement</h2>
              <p>Supported formats: PDF, CSV, Excel (XLSX, XLS)</p>
              
              <div className="file-input-wrapper">
                <input 
                  type="file" 
                  id="file-input"
                  onChange={handleFileChange}
                  accept=".pdf,.csv,.xlsx,.xls"
                />
                <label htmlFor="file-input" className="file-label">
                  {file ? file.name : 'Choose File'}
                </label>
              </div>

              <button 
                className="btn btn-primary"
                onClick={handleUpload}
                disabled={!file || loading}
              >
                {loading ? 'Processing...' : 'Upload & Process'}
              </button>

              <div className="info-box">
                <h3>How it works:</h3>
                <ol>
                  <li>Upload your bank statement (PDF/CSV/Excel)</li>
                  <li>System automatically categorizes all transactions</li>
                  <li>Review and edit categories if needed</li>
                  <li>View analysis charts and summaries</li>
                  <li>Export categorized data for tax filing</li>
                </ol>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'transactions' && (
          <div className="transactions-section">
            <div className="transactions-header">
              <h2>Transactions</h2>
              <div className="transactions-controls">
                <select 
                  className="filter-select"
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                >
                  <option value="All">All Categories</option>
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
                <button className="btn btn-success" onClick={handleExport}>
                  <Download size={18} /> Export to Excel
                </button>
              </div>
            </div>

            <div className="table-container">
              <table className="transactions-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Description</th>
                    <th>Amount</th>
                    <th>Type</th>
                    <th>Category</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTransactions.map((transaction, index) => {
                    const actualIndex = transactions.indexOf(transaction);
                    return (
                      <tr key={index}>
                        <td>{transaction.date}</td>
                        <td className="description">{transaction.description}</td>
                        <td className="amount">₹{transaction.amount.toLocaleString('en-IN')}</td>
                        <td>
                          <span className={`badge ${transaction.type === 'Credit' ? 'badge-success' : 'badge-danger'}`}>
                            {transaction.type}
                          </span>
                        </td>
                        <td>
                          {editingIndex === actualIndex ? (
                            <select 
                              value={transaction.category}
                              onChange={(e) => handleCategoryChange(actualIndex, e.target.value)}
                              autoFocus
                            >
                              {categories.map(cat => (
                                <option key={cat} value={cat}>{cat}</option>
                              ))}
                            </select>
                          ) : (
                            <span className="category-badge">{transaction.category}</span>
                          )}
                        </td>
                        <td>
                          {editingIndex === actualIndex ? (
                            <button 
                              className="btn-icon"
                              onClick={() => setEditingIndex(null)}
                            >
                              <X size={16} />
                            </button>
                          ) : (
                            <button 
                              className="btn-icon"
                              onClick={() => setEditingIndex(actualIndex)}
                            >
                              <Edit2 size={16} />
                            </button>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'analysis' && analysis && (
          <div className="analysis-section">
            <div className="summary-cards">
              <div className="summary-card card-green">
                <h3>Total Credit</h3>
                <p className="amount">₹{analysis.total_credit?.toLocaleString('en-IN') || 0}</p>
              </div>
              <div className="summary-card card-red">
                <h3>Total Debit</h3>
                <p className="amount">₹{analysis.total_debit?.toLocaleString('en-IN') || 0}</p>
              </div>
              <div className="summary-card card-blue">
                <h3>Net Balance</h3>
                <p className="amount">₹{analysis.net_balance?.toLocaleString('en-IN') || 0}</p>
              </div>
            </div>

            <div className="charts-grid">
              <div className="chart-card">
                <h3>Expenses by Category</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={analysis.category_summary}
                      dataKey="total_amount"
                      nameKey="category"
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      label={(entry) => `${entry.category}: ₹${entry.total_amount.toLocaleString('en-IN')}`}
                    >
                      {analysis.category_summary?.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `₹${value.toLocaleString('en-IN')}`} />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-card">
                <h3>Category-wise Spending</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={analysis.category_summary}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="category" angle={-45} textAnchor="end" height={100} />
                    <YAxis />
                    <Tooltip formatter={(value) => `₹${value.toLocaleString('en-IN')}`} />
                    <Bar dataKey="total_amount" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-card full-width">
                <h3>Monthly Spending Trend</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={analysis.monthly_summary}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip formatter={(value) => `₹${value.toLocaleString('en-IN')}`} />
                    <Legend />
                    <Bar dataKey="total_amount" fill="#82ca9d" name="Total Amount" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="table-card full-width">
                <h3>Top 10 Expenses</h3>
                <table className="analysis-table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Description</th>
                      <th>Category</th>
                      <th>Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analysis.top_expenses?.map((expense, index) => (
                      <tr key={index}>
                        <td>{expense.date}</td>
                        <td>{expense.description}</td>
                        <td><span className="category-badge">{expense.category}</span></td>
                        <td className="amount">₹{expense.amount.toLocaleString('en-IN')}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="export-section">
              <button className="btn btn-success btn-lg" onClick={handleExport}>
                <Download size={20} /> Export Complete Report
              </button>
            </div>
          </div>
        )}
      </div>

      <footer className="App-footer">
        <p>Bank Statement Analyzer v1.0 - Built for simplifying tax filing</p>
      </footer>
    </div>
  );
}

export default App;
