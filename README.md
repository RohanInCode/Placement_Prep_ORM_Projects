# 💸 FINTRACK PRO – CLI Finance Manager

FinTrack Pro is a simple Command Line based Personal Finance Management System built using **Python, SQLite, and SQLAlchemy ORM**.

It helps users track daily expenses, manage subscriptions, monitor monthly budgets, and generate financial analytics directly from the terminal.

---

## 🚀 Features

✅ Add Expense  
✅ Update Expense  
✅ Delete Expense  
✅ Search Expense by Date  
✅ Category-wise Expense Analytics (Raw SQL)  
✅ Subscription Tracking  
✅ Monthly Budget Limit & Alerts  
✅ Persistent SQLite Storage  

---

## 🛠 Technologies Used

- Python
- SQLite Database
- SQLAlchemy ORM
- Raw SQL Queries
- CLI Interface

---

## 🗄 Database Design

### Tables

### 1. categories
- id (PK)
- name

### 2. expenses
- id (PK)
- title
- amount
- date
- category_id (FK)

### 3. subscriptions
- id (PK)
- name
- amount
- next_date

### 4. budgets
- id (PK)
- month
- limit_amount

---

## 🔗 Relationships

Category 1 ---- N Expenses

---

## ⚙️ Installation

### Step 1 – Install dependencies
```bash
pip install sqlalchemy

---
### Step 2 -- Run the program

python main.py