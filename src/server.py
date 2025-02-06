import logging
import re
import socket
from datetime import datetime
from multiprocessing import Process
from typing import Tuple, Optional

from config.config import Config
from src.commands.accountManager import AccountManager


class TCPServer:
    def __init__(self):
        config = Config()
        self.server_ip = config.ip
        self.port = int(config.port)
        self.shutdown = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.port))
        self.server_socket.listen(5)
        logging.info(f"Server initialized on {self.server_ip}:{self.port}")

    def shutdown_command(self):

        self.shutdown = True
        return "Server shutting down."

    def handle_client(self, client_socket):
        buffer = ""
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')

                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    message = message.strip().lower()
                    if not message:
                        continue
                    logging.info(f"Received {message}")



                    commands = {
                        "date": lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "help": lambda: "Available commands: date, help,BC,AC AD, shutdown-server",
                        "bc": lambda: f"BC {self.handle_bank_code}",
                        "ac": lambda: f"AC {self.handle_account_create}",
                        "ad": lambda: f"AD {self.handle_account_deposit()}",
                        "shutdown-server": self.shutdown_command
                    }

                    cmd = message.replace('\r', '').replace('\n', '')


                    response = commands.get(cmd, lambda: "Error: Unknown command. Type 'help' for a list of commands.")()
                    client_socket.send((response + "\n").encode('utf-8'))
            except Exception as e:
                logging.error(f"Exception in handle_client: {e}")
                break
        client_socket.close()

    def run(self):
        logging.info(f"Server listening on {self.server_ip}:{self.port}")
        try:
            while not self.shutdown:
                client_socket, client_address = self.server_socket.accept()
                logging.info(f"Connected to {client_address}")

                process = Process(target=self.handle_client, args=(client_socket,))
                process.daemon = True
                process.start()

                client_socket.close()
        except KeyboardInterrupt:
            logging.error("Server interrupted by KeyboardInterrupt.")
        finally:
            self.server_socket.close()
            logging.info("Server shut down.")

    def add_account(self,bank_code,acc_number):

        logging.info("Account added.")

    def account_deposit(self,bank_code,acc_number,balance):
        manager = AccountManager(bank_code=bank_code, acc_number=acc_number,balance=balance)
        manager.update()
        logging.info("Account added.")

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

    def handle_bank_code(self):
        """Handle BC command"""
        return "BC", self.server_ip

    def handle_account_create(self, parts: list) -> Tuple[str, dict]:
        """Handle AC command"""
        manager = AccountManager(bank_code=list[0], acc_number=list[1])
        manager.save()
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





