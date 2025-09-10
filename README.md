# Expense Tracker - Python-Based Personal Finance Analysis Tool

## Project Overview

The Expense Tracker is a Python-based desktop application developed as part of an SY internship under the Department of Information Technology at K. J. Somaiya College of Engineering. It enables users to record, manage, and analyze personal financial data using a GUI interface with integrated database support and visualization features.

This tool facilitates structured logging of daily expenses and provides meaningful insights through analytical features, bridging the gap between raw data and actionable financial understanding.

## Key Features

- GUI-based interface developed using Tkinter
- Expense logging with the following attributes:
  - Date
  - Payee
  - Category (e.g., Food, Stationery, Fees, Clothing, Others)
  - Amount
  - Mode of Payment
- MySQL database integration with persistent data storage
- Full CRUD operations: Add, View, Edit, Delete
- Matplotlib-based visualizations of spending by category
- Sentence conversion of expenses for easier interpretation
- Bulk deletion and form field validation features

## Technologies Used

- Python 3
- Tkinter (Graphical User Interface)
- MySQL (Relational Database Management)
- Matplotlib (Data Visualization)

## Database Schema

The application uses a MySQL table named `ExpenseTracker` with the following fields:

| Field           | Type            | Description                       |
|----------------|------------------|-----------------------------------|
| ID              | INT (PK, AUTO_INCREMENT) | Unique identifier for each record |
| Date            | DATE             | Date of the transaction            |
| Payee           | VARCHAR(255)     | Entity to whom payment is made     |
| Description     | TEXT             | Category of the expense            |
| Amount          | FLOAT            | Amount spent                       |
| ModeOfPayment   | VARCHAR(255)     | Mode used for payment              |

## Installation and Setup

### Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages:
  - `mysql-connector-python`
  - `matplotlib`
  - `tkinter`
  - `tkcalendar`
  - `Pillow`

### Installation & Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/Elysian0987/Expense-Tracker
cd Expense-Tracker
```

#### 2. Install Required Dependencies

```bash
pip install mysql-connector-python matplotlib tkcalendar pillow
```

#### 3. Database Setup

##### Step 1: Create Database
Connect to your MySQL server and create a new database:

```sql
CREATE DATABASE database1;
```

##### Step 2: Select Database
```sql
USE database1;
```

##### Step 3: Create Table Schema
Run the following SQL script to create the required table structure:

```sql
CREATE TABLE ExpenseTracker (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Date DATE NOT NULL,
    Payee VARCHAR(255) NOT NULL,
    Description TEXT,
    Amount FLOAT NOT NULL,
    ModeOfPayment VARCHAR(255)
);
```

#### 4. Configure MySQL Credentials

Open the `expense_tracker.py` file and update the database connection details with your MySQL credentials:

```python
db = mysql.connector.connect(
    host="localhost",
    user="your_username",        # Replace with your MySQL username
    password="your_password",    # Replace with your MySQL password
    database="database1"
)
```

#### 5. Run the Application

```bash
python expense_tracker.py
```

## Usage Guide

- Add a new expense by filling in all fields and selecting the appropriate category and payment method.
- View all expenses in the scrollable table.
- Edit or delete selected records directly from the table.
- Use "Convert to Words" to view expense details in natural language before confirming.
- Use the visualization feature to generate a bar chart of expenses by category.
- Clear all fields or delete all records using respective actions.

## Learning Outcomes

This project was developed as part of a focused internship module, emphasizing:

- GUI programming using Tkinter
- Relational database integration using MySQL
- Data visualization using Matplotlib
- Real-world software design and development practices
- Collaborative version control via GitHub

## Future Enhancements

- User authentication and session management
- Multi-user database support
- Export data as CSV or PDF
- Budget limit tracking and alerts
- Time-series analytics for trends across custom periods
- Modular code architecture and error logging

## Acknowledgments

Developed under the guidance of Prof. Vaibhav Chunekar and Prof. Anagha Raich as part of the in-house internship at K. J. Somaiya College of Engineering, Department of Information Technology.

## Contributing

While this project was completed as part of an academic internship, contributions or suggestions for improvement are still welcome.

If you'd like to contribute, please follow these steps:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is open-source under the terms of the MIT License. See the [LICENSE](LICENSE.md) file for details.
