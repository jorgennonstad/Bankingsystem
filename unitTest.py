from Bankingsystem import BankAccount, SavingsAccount, CheckingAccount, convert_to_float
import unittest

# ==========================
# BankAccount Tests
# ==========================
class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Alice", 1000)

    # --------------------------
    # Normal operations
    # --------------------------
    def test_deposit(self):
        result = self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)
        self.assertIn("500.00 kr was added", result)

    def test_withdraw(self):
        result = self.account.withdraw(300)
        self.assertEqual(self.account.balance, 700)
        self.assertIn("300.00 kr withdrawn", result)

    def test_over_withdraw(self):
        result = self.account.withdraw(2000)
        self.assertEqual(self.account.balance, 1000)
        self.assertIn("Withdrawal amount exceeds your current balance", result)

    def test_account_info(self):
        info = self.account.account_info()
        self.assertIn("Alice", info)
        self.assertIn("1000.00 kr", info)
    
    # --------------------------
    # Negative values tests
    # --------------------------
    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-500)

    def test_withdraw_negative(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-300)

    # --------------------------
    # Type conversion / string input tests
    # --------------------------
    def test_deposit_string_number(self):
        result = self.account.deposit("500")
        self.assertEqual(self.account.balance, 1500)
        self.assertIn("500.00 kr was added", result)

    def test_withdraw_string_number(self):
        result = self.account.withdraw("200")
        self.assertEqual(self.account.balance, 800)
        self.assertIn("200.00 kr withdrawn", result)

    def test_init_string_balance(self):
        acc = BankAccount("Eve", "2000")
        self.assertEqual(acc.balance, 2000)

    def test_deposit_invalid_string(self):
        with self.assertRaises(TypeError):
            self.account.deposit("hello")

    def test_withdraw_invalid_string(self):
        with self.assertRaises(TypeError):
            self.account.withdraw("world")

    def test_init_invalid_balance(self):
        with self.assertRaises(TypeError):
            BankAccount("Eve", "abc")



# ==========================
# SavingsAccount Tests
# ==========================
class TestSavingsAccount(unittest.TestCase):

    def setUp(self):
        self.sa_default = SavingsAccount("Bob", 2000, 0.05)
        self.sa_zero = SavingsAccount("Bob", 2000, 0.0)
        self.sa_full = SavingsAccount("Bob", 2000, 1.0)

    # --------------------------
    # Normal operations
    # --------------------------
    def test_deposit_with_interest(self):
        self.sa_default.deposit(1000)
        self.assertEqual(self.sa_default.balance, 3000)

    def test_withdraw_with_interest(self):
        self.sa_default.withdraw(500)
        self.assertEqual(self.sa_default.balance, 1500)

    def test_over_withdraw(self):
        result = self.sa_default.withdraw(5000)
        self.assertIn("Withdrawal amount exceeds your current balance", result)
        self.assertEqual(self.sa_default.balance, 2000)

    def test_apply_interest_5_percent(self):
        result = self.sa_default.apply_interest()
        self.assertAlmostEqual(self.sa_default.balance, 2000*1.05)
        self.assertIn("Applied 5.00% interest", result)

    def test_apply_interest_0_percent(self):
        result = self.sa_zero.apply_interest()
        self.assertEqual(self.sa_zero.balance, 2000)
        self.assertIn("Applied 0.00% interest", result)

    def test_apply_interest_100_percent(self):
        result = self.sa_full.apply_interest()
        self.assertEqual(self.sa_full.balance, 2000*2)
        self.assertIn("Applied 100.00% interest", result)

    # --------------------------
    # Account info
    # --------------------------
    def test_account_info_default(self):
        info = self.sa_default.account_info()
        self.assertIn("Bob", info)
        self.assertIn("Interest Rate: 5.00%", info)

    def test_account_info_zero_interest(self):
        info = self.sa_zero.account_info()
        self.assertIn("Interest Rate: 0.00%", info)

    def test_account_info_full_interest(self):
        info = self.sa_full.account_info()
        self.assertIn("Interest Rate: 100.00%", info)

    # --------------------------
    # Negative values tests
    # --------------------------
    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.sa_default.deposit(-500)

    def test_withdraw_negative(self):
        with self.assertRaises(ValueError):
            self.sa_default.withdraw(-300)

    # --------------------------
    # Type conversion / string input tests
    # --------------------------
    def test_deposit_string_number(self):
        result = self.sa_default.deposit("500")
        self.assertEqual(self.sa_default.balance, 2500)
        self.assertIn("500.00 kr was added", result)

    def test_withdraw_string_number(self):
        result = self.sa_default.withdraw("200")
        self.assertEqual(self.sa_default.balance, 1800)
        self.assertIn("200.00 kr withdrawn", result)

    def test_init_string_balance(self):
        acc = SavingsAccount("Eve", "2000", 0.05)
        self.assertEqual(acc.balance, 2000)

    def test_deposit_invalid_string(self):
        with self.assertRaises(TypeError):
            self.sa_default.deposit("hello")

    def test_withdraw_invalid_string(self):
        with self.assertRaises(TypeError):
            self.sa_default.withdraw("world")

    def test_init_invalid_balance(self):
        with self.assertRaises(TypeError):
            SavingsAccount("Eve", "abc", 0.05)

    def test_init_invalid_interest_rate(self):
        with self.assertRaises(TypeError):
            SavingsAccount("Grace", 1000, "xyz")


# ==========================
# CheckingAccount Tests
# ==========================
class TestCheckingAccount(unittest.TestCase):

    def setUp(self):
        self.ca = CheckingAccount("Charlie", 1000, 20)

    # --------------------------
    # Normal operations
    # --------------------------
    def test_deposit(self):
        result = self.ca.deposit(500)
        self.assertEqual(self.ca.balance, 1500)
        self.assertIn("500.00 kr was added", result)

    def test_withdraw(self):
        result = self.ca.withdraw(100)
        self.assertEqual(self.ca.balance, 880)
        self.assertIn("100.00 kr withdrawn with 20.00 kr fee", result)

    def test_over_withdraw(self):
        result = self.ca.withdraw(2000)
        self.assertIn("Withdrawal + fee exceeds balance", result)
        self.assertEqual(self.ca.balance, 1000)

    def test_account_info(self):
        info = self.ca.account_info()
        self.assertIn("Charlie", info)
        self.assertIn("Transaction Fee: 20.00 kr", info)

    # --------------------------
    # Negative values tests
    # --------------------------
    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.ca.deposit(-500)

    def test_withdraw_negative(self):
        with self.assertRaises(ValueError):
            self.ca.withdraw(-100)

    # --------------------------
    # Type conversion / string input tests
    # --------------------------
    def test_deposit_string_number(self):
        result = self.ca.deposit("500")
        self.assertEqual(self.ca.balance, 1500)
        self.assertIn("500.00 kr was added", result)

    def test_withdraw_string_number(self):
        result = self.ca.withdraw("100")
        self.assertEqual(self.ca.balance, 880)
        self.assertIn("100.00 kr withdrawn with 20.00 kr fee", result)

    def test_init_string_balance_and_fee(self):
        acc = CheckingAccount("Eve", "2000", "15")
        self.assertEqual(acc.balance, 2000)
        self.assertEqual(acc.transaction_fee, 15)

    def test_deposit_invalid_string(self):
        with self.assertRaises(TypeError):
            self.ca.deposit("hello")

    def test_withdraw_invalid_string(self):
        with self.assertRaises(TypeError):
            self.ca.withdraw("world")

    def test_init_invalid_balance(self):
        with self.assertRaises(TypeError):
            CheckingAccount("Eve", "abc", 10)

    def test_init_invalid_fee(self):
        with self.assertRaises(TypeError):
            CheckingAccount("Ivy", 1000, "fee")



# ==========================
# Convert to float Tests
# ==========================
class TestConvertToFloat(unittest.TestCase):

    def test_valid_numbers(self):
        self.assertEqual(convert_to_float(1000), 1000.0)
        self.assertEqual(convert_to_float("1000"), 1000.0)
        self.assertEqual(convert_to_float(99.99), 99.99)
        self.assertEqual(convert_to_float("123.45"), 123.45)

    def test_invalid_numbers(self):
        with self.assertRaises(TypeError):
            convert_to_float("Fivehundred", "Deposit amount")
        with self.assertRaises(TypeError):
            convert_to_float("100s0", "Balance")
        with self.assertRaises(TypeError):
            convert_to_float("abc123", "Value")

# ==========================
# Account Holder Type Variations
# ==========================
class TestAccountHolderTypes(unittest.TestCase):

    def test_account_holder_int(self):
        acc = BankAccount(12345, 1000)
        self.assertEqual(acc.account_holder, "12345")  # should be string

    def test_account_holder_float(self):
        acc = BankAccount(123.45, 1000)
        self.assertEqual(acc.account_holder, "123.45")  # should be string


if __name__ == "__main__":
    unittest.main()
