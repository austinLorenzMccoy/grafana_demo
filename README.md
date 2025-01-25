# 🏦 Grafana Banking Transaction Simulator & Analytics Dashboard

## 📊 Project Overview

This project is a comprehensive banking transaction data generation and visualization system that demonstrates real-time financial data analysis using Python, PostgreSQL, and Grafana.

### 🌟 Key Features
- Realistic banking transaction data generation
- Automatic rule-based transaction processing
- AWS RDS PostgreSQL integration
- Grafana dashboard for comprehensive financial insights

## 🚀 Technology Stack
- **Backend**: Python 3.8+
- **Database**: PostgreSQL (AWS RDS)
- **Data Generation**: Faker Library
- **Visualization**: Grafana
- **Logging**: Python Logging Module

## 🔧 Prerequisites
- Python 3.8+
- PostgreSQL
- AWS RDS Account
- Grafana
- Dependencies listed in `requirements.txt`

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/austinLorenzMccoy/grafana_demo.git
cd grafana_demo
```

### 2. Create Virtual Environment
```bash
python3 -m venv grafana_env
source grafana_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
export DB_HOST=your-rds-endpoint
export DB_USER=your-username
export DB_PASSWORD=your-password
```

## 🔍 Project Components

### 1. Data Generation Script (`app.py`)
- Generates synthetic banking transaction data
- Implements transaction rule processing
- Supports configurable data generation

### 2. Transaction Rules
- Rule 1: Reject transactions over $100 for non-blacklisted accounts
- Rule 2: Reject transactions from blacklisted accounts

### 3. Grafana Dashboard
Visualizes key metrics:
- Total Approved/Rejected Transaction Amounts
- Transaction Type Distribution
- Rules Triggered Analysis
- Blacklisted Account Transactions

## 🖥️ Running the Application
```bash
python app.py
```

## 📈 Grafana Dashboard Configuration
1. Connect Grafana to PostgreSQL
2. Import provided dashboard JSON
3. Configure data sources
4. Customize visualizations

## 🛡️ Security Considerations
- Use environment variables for credentials
- Restrict database access
- Implement proper network security groups

## 📊 Sample Queries Included
- Total Approved Amount
- Rejected Transaction Amount
- Transaction Type Analysis
- Rules Triggered Breakdown
- Blacklisted Account Transactions

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📜 License
MIT License

## 🚨 Disclaimer
This is a demonstration project. Do not use production credentials or sensitive information.

## 📬 Contact
Austin Lorenz McCoy
- GitHub: [@austinLorenzMccoy](https://github.com/austinLorenzMccoy)
- Email: chibuezeagustine23@gmail.com

---

**Made with ❤️ for Data Visualization and Banking Analytics**