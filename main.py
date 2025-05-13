import sys
import os
from typing import Optional
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from app.database import Database
from app.transaction import Transaction
from app.report import generate_report
from app.config import save_currency_symbol, load_currency_symbol
from app.budget import Budget
from app.alert import Alerts
from export import export_report_to_csv
from sns.aws_sns import SNSNotifier

# Constants
MENU_OPTIONS = {
    '1': 'Add Transaction',
    '2': 'View Transactions',
    '3': 'Generate Report',
    '4': 'Manage Budget',
    '5': 'Clear All Transactions',
    '6': 'Export Report to CSV',
    '7': 'Exit'
}

def main_menu() -> str:
    """Display the main menu and get user choice."""
    print("\nPersonal Finance Tracker")
    for key, value in MENU_OPTIONS.items():
        print(f"{key}. {value}")
    return input("Choose an option: ")

def validate_amount(amount_str: str) -> float:
    """Validate and convert amount input to float."""
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return amount
    except ValueError as e:
        raise ValueError(f"Invalid amount: {e}")

def add_transaction(db: Database, currency_symbol: str, alerts: Alerts) -> None:
    """Add a new transaction to the database."""
    try:
        amount = validate_amount(input("Enter amount: "))
        category = input("Enter category: ").strip()
        description = input("Enter description: ").strip()
        transaction_type = input("Enter type (income/expense): ").lower()

        if not category or not description:
            raise ValueError("Category and description cannot be empty")
        if transaction_type not in ['income', 'expense']:
            raise ValueError("Transaction type must be 'income' or 'expense'")

        transaction = Transaction(amount, category, description, transaction_type)
        db.add_transaction(transaction)
        print(f"Transaction added successfully! {currency_symbol}{amount:.2f}")

        transactions = db.get_all_transactions()
        alerts.check_alerts(transactions)
    except ValueError as e:
        print(f"Error: {e}")

def view_transactions(db: Database, currency_symbol: str) -> None:
    """Display all transactions."""
    transactions = db.get_all_transactions()
    if not transactions:
        print("No transactions found.")
        return
    
    for txn in transactions:
        print(f"{txn.date}: {txn.type.capitalize()} - {currency_symbol}{txn.amount:.2f} - {txn.category} - {txn.description}")

def manage_budget(budget: Budget, currency_symbol: str) -> None:
    """Manage budget settings."""
    while True:
        print("\nBudget Management")
        print("1. Set Budget")
        print("2. View Budgets")
        print("3. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            try:
                category = input("Enter category: ").strip()
                amount = validate_amount(input("Enter budget amount: "))
                budget.set_budget(category, amount)
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '2':
            budget.view_budgets()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def setup_sns() -> tuple[Optional[SNSNotifier], str]:
    """Setup SNS notifications if requested."""
    use_sns = input("Do you want to enable AWS SNS alerts? (yes/no): ").strip().lower() == 'yes'
    email = input("Enter your email address to receive notifications: ").strip()
    
    if use_sns:
        sns_notifier = SNSNotifier()
        sns_notifier.setup(email)
        return sns_notifier, email
    return None, email

def main() -> None:
    """Main application entry point."""
    try:
        currency_symbol = input("Enter your preferred currency symbol: ").strip()
        save_currency_symbol(currency_symbol)
        CURRENCY_SYMBOL = load_currency_symbol()

        db = Database()
        budget = Budget(CURRENCY_SYMBOL)
        alerts = Alerts(budget)

        sns_notifier, email = setup_sns()

        while True:
            choice = main_menu()
            if choice == '1':
                add_transaction(db, CURRENCY_SYMBOL, alerts)
            elif choice == '2':
                view_transactions(db, CURRENCY_SYMBOL)
            elif choice == '3':
                generate_report(db, CURRENCY_SYMBOL)
            elif choice == '4':
                manage_budget(budget, CURRENCY_SYMBOL)
            elif choice == '5':
                db.clear_transactions()
            elif choice == '6':
                export_report_to_csv(db, CURRENCY_SYMBOL)
            elif choice == '7':
                transactions = db.get_all_transactions()
                alerts.check_alerts(transactions)
                print("Thank you for using Personal Finance Tracker!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
