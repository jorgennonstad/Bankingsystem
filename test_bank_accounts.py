from Bankingsystem import BankAccount, SavingsAccount, CheckingAccount


# ==========================
# Helper function: Run automated tests
# ==========================
def run_test(title, func, expected=None):
    """
    Simple automated test runner with expected output or exception.
    """
    try:
        result = func()
        if expected is None:
            print(f"✅ {title}: PASSED")
        elif isinstance(expected, type) and issubclass(expected, Exception):
            print(f"❌ {title}: FAILED (expected exception {expected.__name__})")
        elif result == expected:
            print(f"✅ {title}: PASSED")
        else:
            print(f"❌ {title}: FAILED\n   Expected: {expected}\n   Got:      {result}")
    except Exception as e:
        if isinstance(expected, type) and isinstance(e, expected):
            print(f"✅ {title}: PASSED (raised {expected.__name__})")
        else:
            print(f"❌ {title}: ERROR\n   {e}")

# ==========================
# AUTOMATED EXPECTED RESULTS TESTS
# ==========================
print("\n==================== AUTOMATED TESTS ====================")

# --- BankAccount Tests ---
print("\n--- BankAccount Tests ---")
ba = BankAccount("Alice", 1000)
run_test("Deposit 500", lambda: ba.deposit(500), "500.00 kr was added. Total balance: 1500.00 kr")
run_test("Withdraw 300", lambda: ba.withdraw(300), "300.00 kr withdrawn. Total balance: 1200.00 kr")
run_test("Over-withdraw", lambda: ba.withdraw(2000), "Withdrawal amount exceeds your current balance of 1200.00 kr")
run_test("Account Info", lambda: ba.account_info(), "Account Holder: Alice, Balance: 1200.00 kr")


# --- SavingsAccount Tests ---
print("\n--- SavingsAccount Tests ---")
# Create multiple savings accounts with different interest rates
sa_5 = SavingsAccount("Bob", 2000, 0.05)
sa_0 = SavingsAccount("Carol", 2000, 0.0)
sa_100 = SavingsAccount("Dave", 2000, 1.0)

run_test("Deposit 1000 (5% interest)", lambda: sa_5.deposit(1000), "1000.00 kr was added. Total balance: 3000.00 kr")
run_test("Withdraw 500 (5% interest)", lambda: sa_5.withdraw(500), "500.00 kr withdrawn. Total balance: 2500.00 kr")
run_test("Over-withdraw (5% interest)", lambda: sa_5.withdraw(3000), "Withdrawal amount exceeds your current balance of 2500.00 kr")
run_test("Apply 5% Interest", lambda: sa_5.apply_interest(), "Applied 5.00% interest. Old balance: 2500.00 kr, Interest: 125.00 kr, New balance: 2625.00 kr")
run_test("Account Info (5% interest)", lambda: sa_5.account_info(), "Account Holder: Bob, Balance: 2625.00 kr, Interest Rate: 5.00%")
run_test("Apply 0% Interest", lambda: sa_0.apply_interest(), "Applied 0.00% interest. Old balance: 2000.00 kr, Interest: 0.00 kr, New balance: 2000.00 kr")
run_test("Apply 100% Interest", lambda: sa_100.apply_interest(), "Applied 100.00% interest. Old balance: 2000.00 kr, Interest: 2000.00 kr, New balance: 4000.00 kr")
run_test("Account Info (0% interest)", lambda: sa_0.account_info(), "Account Holder: Carol, Balance: 2000.00 kr, Interest Rate: 0.00%")
run_test("Account Info (100% interest)", lambda: sa_100.account_info(), "Account Holder: Dave, Balance: 4000.00 kr, Interest Rate: 100.00%")


# --- CheckingAccount Tests ---
print("\n--- CheckingAccount Tests ---")
ca = CheckingAccount("Charlie", 1000, 20)
run_test("Deposit 500", lambda: ca.deposit(500), "500.00 kr was added. Total balance: 1500.00 kr")
run_test("Withdraw 100 (with fee)", lambda: ca.withdraw(100), "100.00 kr withdrawn with 20.00 kr fee. Total balance: 1380.00 kr")
run_test("Over-withdraw", lambda: ca.withdraw(2000), "Withdrawal + fee exceeds balance (1380.00 kr)")
run_test("Account Info", lambda: ca.account_info(), "Account Holder: Charlie, Balance: 1380.00 kr, Transaction Fee: 20.00 kr")


# --- Type Conversion & Error Handling Tests ---
print("\n--- Type Conversion & Error Handling Tests ---")
# Valid numeric strings
run_test("Deposit '500' as string", lambda: ba.deposit("500"), "500.00 kr was added. Total balance: 1700.00 kr")
run_test("Withdraw '200' as string", lambda: ba.withdraw("200"), "200.00 kr withdrawn. Total balance: 1500.00 kr")
run_test("Initialize with '2000' string balance", lambda: BankAccount("Eve", "2000"))

# Invalid strings should raise TypeError
run_test("Deposit 'hello' invalid string", lambda: ba.deposit("hello"), TypeError)
run_test("Withdraw 'world' invalid string", lambda: ba.withdraw("world"), TypeError)
run_test("Initialize with 'abc' invalid balance", lambda: BankAccount("Eve", "abc"), TypeError)
run_test("SavingsAccount interest_rate invalid 'xyz'", lambda: SavingsAccount("Grace", 1000, "xyz"), TypeError)
run_test("CheckingAccount transaction_fee invalid 'fee'", lambda: CheckingAccount("Ivy", 1000, "fee"), TypeError)

# Account holder type variations
run_test("Account holder as int", lambda: BankAccount(123, 100), None)
run_test("Account holder as float", lambda: BankAccount(45.67, 100), None)


# --- Negative Value Tests ---
print("\n--- Negative Value Tests ---")
run_test("Deposit -500 should raise ValueError", lambda: ba.deposit(-500), ValueError)
run_test("Withdraw -300 should raise ValueError", lambda: ba.withdraw(-300), ValueError)
run_test("CheckingAccount withdraw -100 should raise ValueError", lambda: ca.withdraw(-100), ValueError)
