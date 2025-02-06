import re
from typing import Tuple, Optional


class BankCommandParser:
    def __init__(self):
        # Dictionary mapping command codes to their handler methods
        self.commands = {
            "BC": self.handle_bank_code,
            "AC": self.handle_account_create,
            "AD": self.handle_account_deposit,
            "AW": self.handle_account_withdrawal,
            "AB": self.handle_account_balance,
            "AR": self.handle_account_remove,
            "BA": self.handle_bank_amount,
            "BN": self.handle_bank_number
        }

    def parse_command(self, command: str) -> Tuple[str, Optional[dict]]:
        """
        Parse the input command and return the command type and parameters
        Returns: Tuple of (command_type, parameters_dict)
        """
        command = command.strip()
        parts = command.split()

        if not parts:
            return "ER", {"message": "Empty command"}

        command_type = parts[0].upper()

        if command_type not in self.commands:
            return "ER", {"message": "Unknown command"}

        return self.commands[command_type](parts)

    def parse_account_number(self, account_str: str) -> Tuple[bool, Optional[dict]]:
        """Validate and parse account number in format number/ip_address"""
        if not account_str or '/' not in account_str:
            return False, None

        acc_num, bank_code = account_str.split('/')

        # Validate account number (10000-99999)
        if not acc_num.isdigit() or not (10000 <= int(acc_num) <= 99999):
            return False, None

        # Basic IP address validation
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(ip_pattern, bank_code):
            return False, None

        return True, {"account_number": acc_num, "bank_code": bank_code}

    def handle_bank_code(self, parts: list) -> Tuple[str, dict]:
        """Handle BC command"""
        return "BC", {}

    def handle_account_create(self, parts: list) -> Tuple[str, dict]:
        """Handle AC command"""
        return "AC", {}

    def handle_account_deposit(self, parts: list) -> Tuple[str, dict]:
        """Handle AD command"""
        if len(parts) != 3:
            return "ER", {"message": "Invalid command format"}

        valid, account_info = self.parse_account_number(parts[1])
        if not valid:
            return "ER", {"message": "Invalid account number format"}

        try:
            amount = int(parts[2])
            if amount <= 0:
                return "ER", {"message": "Amount must be positive"}
        except ValueError:
            return "ER", {"message": "Invalid amount format"}

        return "AD", {**account_info, "amount": amount}

    def handle_account_withdrawal(self, parts: list) -> Tuple[str, dict]:
        """Handle AW command"""
        if len(parts) != 3:
            return "ER", {"message": "Invalid command format"}

        valid, account_info = self.parse_account_number(parts[1])
        if not valid:
            return "ER", {"message": "Invalid account number format"}

        try:
            amount = int(parts[2])
            if amount <= 0:
                return "ER", {"message": "Amount must be positive"}
        except ValueError:
            return "ER", {"message": "Invalid amount format"}

        return "AW", {**account_info, "amount": amount}

    def handle_account_balance(self, parts: list) -> Tuple[str, dict]:
        """Handle AB command"""
        if len(parts) != 2:
            return "ER", {"message": "Invalid command format"}

        valid, account_info = self.parse_account_number(parts[1])
        if not valid:
            return "ER", {"message": "Invalid account number format"}

        return "AB", account_info

    def handle_account_remove(self, parts: list) -> Tuple[str, dict]:
        """Handle AR command"""
        if len(parts) != 2:
            return "ER", {"message": "Invalid command format"}

        valid, account_info = self.parse_account_number(parts[1])
        if not valid:
            return "ER", {"message": "Invalid account number format"}

        return "AR", account_info

    def handle_bank_amount(self, parts: list) -> Tuple[str, dict]:
        """Handle BA command"""
        return "BA", {}

    def handle_bank_number(self, parts: list) -> Tuple[str, dict]:
        """Handle BN command"""
        return "BN", {}


# Create parser instance
parser = BankCommandParser()

# Example commands
commands = [
    "BC",
    "AC",
    "AD 10001/10.1.2.3 3000",
    "AW 10001/10.1.2.3 2000",
    "AB 10001/10.1.2.3",
    "AR 10001/10.1.2.3",
    "BA",
    "BN"
]

# Parse and process commands
for cmd in commands:
    command_type, params = parser.parse_command(cmd)
    print(f"Command: {cmd}")
    print(f"Type: {command_type}")
    print(f"Parameters: {params}")
    print("-" * 50)
