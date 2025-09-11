# ==========================
# Helper function for type conversion
# ==========================
def convert_to_float(value, name="Value"):
    """
    Attempts to convert value to float.
    Raises TypeError if conversion fails.
    """
    try:
        return float(value)
    except ValueError:
        raise TypeError(f"{name} must be a number or convertible to a number")


# ==========================
# Base Class: BankAccount
# ==========================
class BankAccount:
    """
    Base class for a simple bank account
    """
    def __init__(self, account_holder, balance=0):
        self.account_holder = str(account_holder)
        self.balance = convert_to_float(balance, "Balance")

    def deposit(self, amount):
        """
        Deposit money into the account.
        """
        amount = convert_to_float(amount, "Deposit amount")
        if amount < 0:
            raise ValueError("Deposit amount cannot be negative")
        self.balance += amount
        return f"{amount:.2f} kr was added. Total balance: {self.balance:.2f} kr"

    def withdraw(self, amount):
        """
        Withdraw money from the account if sufficient balance exists.
        """
        amount = convert_to_float(amount, "Withdrawal amount")
        if amount < 0:
            raise ValueError("Withdrawal amount cannot be negative")
        if amount <= self.balance:
            self.balance -= amount
            return f"{amount:.2f} kr withdrawn. Total balance: {self.balance:.2f} kr"
        else:
            return f"Withdrawal amount exceeds your current balance of {self.balance:.2f} kr"

    def account_info(self):
        """
        Returns account information.
        """
        return f"Account Holder: {self.account_holder}, Balance: {self.balance:.2f} kr"


# ==========================
# Derived Class: SavingsAccount
# ==========================
class SavingsAccount(BankAccount):
    """
    Savings account with interest rate.
    """
    def __init__(self, account_holder, balance=0, interest_rate=0.02):
        super().__init__(account_holder, balance)
        self.interest_rate = convert_to_float(interest_rate, "Interest rate")

    def apply_interest(self):
        """
        Apply interest to the account balance.
        """
        old_balance = self.balance
        interest_amount = self.balance * self.interest_rate
        self.balance += interest_amount
        return (
            f"Applied {self.interest_rate*100:.2f}% interest. "
            f"Old balance: {old_balance:.2f} kr, Interest: {interest_amount:.2f} kr, "
            f"New balance: {self.balance:.2f} kr"
        )

    def account_info(self):
        """
        Returns account info including interest rate.
        """
        base_info = super().account_info()
        return f"{base_info}, Interest Rate: {self.interest_rate*100:.2f}%"


# ==========================
# Derived Class: CheckingAccount
# ==========================
class CheckingAccount(BankAccount):
    """
    Checking account with a transaction fee on withdrawals.
    """
    def __init__(self, account_holder, balance=0, transaction_fee=1):
        super().__init__(account_holder, balance)
        self.transaction_fee = convert_to_float(transaction_fee, "Transaction fee")

    def withdraw(self, amount):
        """
        Withdraw money including the transaction fee.
        """
        amount = convert_to_float(amount, "Withdrawal amount")
        if amount < 0:
            raise ValueError("Withdrawal amount cannot be negative")

        total = amount + self.transaction_fee
        if total <= self.balance:
            self.balance -= total
            return (
                f"{amount:.2f} kr withdrawn with {self.transaction_fee:.2f} kr fee. "
                f"Total balance: {self.balance:.2f} kr"
            )
        else:
            return f"Withdrawal + fee exceeds balance ({self.balance:.2f} kr)"

    def account_info(self):
        """
        Returns account info including transaction fee.
        """
        base_info = super().account_info()
        return f"{base_info}, Transaction Fee: {self.transaction_fee:.2f} kr"


# ==========================
# Example usage
# ==========================
if __name__ == "__main__":
    # --------------------------
    # Create accounts
    # --------------------------
    ba = BankAccount("Alice", 1000)
    sa = SavingsAccount("Bob", 2000, 0.05)
    ca = CheckingAccount("Charlie", 1000, 20)

    print("\n==================== EXAMPLE USAGE ====================\n")

    # --------------------------
    # BankAccount Example
    # --------------------------
    print("💰 Bank Account (Alice)")
    print(ba.deposit(500))
    print(ba.withdraw(300))
    print(ba.account_info())
    print("-" * 60)

    # --------------------------
    # SavingsAccount Example
    # --------------------------
    print("🏦 Savings Account (Bob, 5% interest)")
    print(sa.apply_interest())
    print(sa.account_info())
    print("-" * 60)

    # --------------------------
    # CheckingAccount Example
    # --------------------------
    print("🏧 Checking Account (Charlie, 20 kr fee)")
    print(ca.withdraw(100))
    print(ca.account_info())
