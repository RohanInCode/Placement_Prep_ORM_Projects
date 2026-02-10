# =====================================
# FINTRACK PRO - CLI FINANCE MANAGER
# =====================================


# ---------- IMPORTS ----------
# Used for DB connection + SQL
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, text

# Used for ORM models + session handling
from sqlalchemy.orm import declarative_base, sessionmaker, relationship



# ---------- DATABASE CONNECTION ----------
# Create SQLite database file
engine = create_engine("sqlite:///expensetracker.db", echo=True)

# Base class
Base = declarative_base()

# Session (like cursor)
Session = sessionmaker(bind=engine)

# Session object
session = Session()



# ---------- TABLE DEFINITIONS ----------

# Category table
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # One category → many expenses
    expenses = relationship("Expense", back_populates="category")



# Expense table
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    amount = Column(Float)  
    date = Column(String)

    # Foreign key linking category
    category_id = Column(Integer, ForeignKey("categories.id")) 

    category = relationship("Category", back_populates="expenses")  



# Subscription table
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float)
    next_date = Column(String)



# Budget table
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True)
    month = Column(String)
    limit_amount = Column(Float)



# Create tables
Base.metadata.create_all(engine)



# ---------- FUNCTIONS ----------

# Add new category
def add_category():
    name = input("Category name: ")
    session.add(Category(name=name))
    session.commit()
    print("✅ Category added")


# Add expense
def add_expense():
    title = input("Expense title: ")
    amount = float(input("Amount: "))
    date = input("Date (YYYY-MM-DD): ")
    category_id = int(input("Category ID: "))

    session.add(Expense(title=title, amount=amount, date=date, category_id=category_id))
    session.commit()
    print("✅ Expense added")


# Update expense
def update_expense():
    eid = int(input("Expense ID: "))

    exp = session.query(Expense).filter(Expense.id == eid).first()

    if exp:
        exp.title = input("New title: ")
        exp.amount = float(input("New amount: "))
        exp.date = input("New date: ")
        session.commit()
        print("✅ Expense updated")
    else:
        print("❌ Expense not found")


# Delete expense
def delete_expense():
    eid = int(input("Expense ID: "))

    exp = session.query(Expense).filter(Expense.id == eid).first()

    if exp:
        session.delete(exp)
        session.commit()
        print("✅ Expense deleted")
    else:
        print("❌ Expense not found")


# Search expenses by date
def search_by_date():
    date = input("Enter date: ")

    expenses = session.query(Expense).filter(Expense.date == date).all()

    for e in expenses:
        print(e.title, "-", e.amount)



# ---------- SUBSCRIPTIONS ----------

def add_subscription():
    name = input("Subscription name: ")
    amount = float(input("Amount: "))
    next_date = input("Next payment date: ")

    session.add(Subscription(name=name, amount=amount, next_date=next_date))
    session.commit()
    print("✅ Subscription added")


def view_subscriptions():
    subs = session.query(Subscription).all()

    for s in subs:
        print(s.name, "-", s.amount, "-", s.next_date)



# ---------- RAW SQL ANALYTICS ----------

def category_report():
    sql = """
    SELECT categories.name, SUM(expenses.amount)
    FROM categories
    JOIN expenses ON categories.id = expenses.category_id
    GROUP BY categories.name
    """

    result = session.execute(text(sql))

    print("\n📊 Category Wise Expense Report")

    for row in result:
        print(row[0], "→ ₹", row[1])



# ---------- BUDGET ----------

def set_budget():
    month = input("Month (YYYY-MM): ")
    limit_amount = float(input("Budget limit: "))

    session.add(Budget(month=month, limit_amount=limit_amount))
    session.commit()
    print("✅ Budget set")


def budget_alert():
    month = input("Month (YYYY-MM): ")

    total = session.execute(
        text("SELECT SUM(amount) FROM expenses WHERE date LIKE :m"),
        {"m": f"{month}%"}
    ).scalar() or 0

    budget = session.query(Budget).filter(Budget.month == month).first()

    if budget and total > budget.limit_amount:
        print("⚠️ Budget exceeded")
    else:
        print("✅ Within budget")



# ---------- CLI MENU ----------

while True:
    print("""
===== FINTRACK PRO =====
1. Add Category
2. Add Expense
3. Update Expense
4. Delete Expense
5. Search Expense by Date
6. Category Expense Report
7. Add Subscription
8. View Subscriptions
9. Set Monthly Budget
10. Budget Alert
11. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        add_category()
    elif choice == "2":
        add_expense()
    elif choice == "3":
        update_expense()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        search_by_date()
    elif choice == "6":
        category_report()
    elif choice == "7":
        add_subscription()
    elif choice == "8":
        view_subscriptions()
    elif choice == "9":
        set_budget()
    elif choice == "10":
        budget_alert()
    elif choice == "11":
        break
    else:
        print("Invalid choice")
