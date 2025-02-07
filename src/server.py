import logging
import re
import socket
from datetime import datetime
from multiprocessing import Process
from typing import Tuple, Optional

from config.config import Config
from src.commands.accountManager import AccountManager
from utils import setup_logging


class TCPServer:
    def __init__(self,config: Config):
        self.config = config
        self.server_ip = config.ip
        self.port = int(config.port)
        self.shutdown = False
        self._setup()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.port))
        self.server_socket.listen(5)
        self.client_timeout = int(config.client_timeout)
        logging.info(f"Server initialized on {self.server_ip}:{self.port}")


        self.command_handlers = {
            "DATE": self.handle_date,
            "HELP": self.handle_help,
            "BC": self.handle_bc,
            "AC": self.handle_account_create,
            "AD": self.handle_account_deposit,
            "AW": self.handle_account_withdrawal,
            "AB": self.handle_account_balance,
            "AR": self.handle_account_remove,
            "BA": self.handle_bank_amount,
            "BN": self.handle_bank_number,
        }

    def _setup(self):
        setup_logging(self.config.logging_level, self.config.logging_file)
        logging.info("Application setup started.")
        try:
            logging.info("Application setup completed.")
        except Exception:
            logging.exception("Application setup failed.")
    def shutdown_command(self) -> str:
        self.shutdown = True
        return "Server shutting down."

    # --- Command Handlers ---

    def handle_date(self, parts: list) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def handle_help(self, parts: list) -> str:
        return ("Available commands: DATE, HELP, BC, AC, AD, AW, AB, AR, BA, BN, ")

    def handle_shutdown(self, parts: list) -> str:
        return self.shutdown_command()

    def handle_bc(self, parts: list) -> str:
        return f"BC {self.handle_bank_code()}"

    def handle_account_create(self, parts: list) -> str:
        """
        Handle the AC command.
        """
        try:
            bank_code = self.server_ip

            # Pass a default value (None) for account_number since it will be auto-generated.
            manager = AccountManager(account_number=None, bank_code=bank_code)
            account_number = manager.save()

            logging.info("Account created.")
            return f"AC {account_number}/{bank_code}"
        except Exception as e:
            logging.exception("Exception occurred in handle_account_create")
            raise "Error processing command."

    def handle_account_deposit(self, parts: list) -> str:
        if len(parts) != 3:
            return ("Error: AD command requires parameters: AD "
                    "account_number/ip_address amount")
        valid, account_info = self.parse_account_number(parts[1])
        if not valid:
            return ("Error: Invalid account string format. Expected format: "
                    "number/ip_address")
        try:
            amount = int(parts[2])
            if amount <= 0:
                return "Error: Amount must be positive."
        except ValueError:
            return "Error: Invalid amount format."
        manager = AccountManager(bank_code=account_info["bank_code"], account_number=account_info["account_number"], balance=amount)
        manager.update()

        return (f"AD")

    def handle_account_withdrawal(self, parts: list) -> str:
        """Perform withdrawal operation via the AccountManager."""
        if len(parts) != 3:
            return ("Error: AW command requires parameters: AW account_number/ip_address amount")

        valid, account_info = self.parse_account_number(parts[1])
        if not valid:
            return ("Error: Invalid account string format. Expected format: number/ip_address")

        try:
            amount = int(parts[2])
            if amount <= 0:
                return "Error: Amount must be positive."
        except ValueError:
            return "Error: Invalid amount format."

        current_balance = self.handle_account_balance(account_info["bank_code"],
                                                      account_info["account_number"])

        if amount <= current_balance:
            new_balance = amount - current_balance
            manager = AccountManager(
                bank_code=account_info["bank_code"],
                account_number=account_info["account_number"],
                balance=new_balance
            )
            manager.update()
            logging.info("Withdrawal processed.")
            return "AW"
        else:
            return "Error: Amount exceeds current balance."

    def handle_account_balance(self, parts: list) -> str:
        """
        Command handler for the AB command.
        Expected command format: AB account_number/ip_address
        This function parses the command, retrieves the account, and returns
        the balance.
        """
        if len(parts) != 2:
            return "Error: AB command requires parameter: account_number/ip_address"

        valid, account_info = self.parse_account_number(parts[1])
        if not valid:
            return ("Error: Invalid account string format. Expected format: "
                    "number/ip_address")

        try:
            # Retrieve the account row using AccountManager's find method.
            account_manager = AccountManager(
                bank_code=account_info["bank_code"],
                account_number=account_info["account_number"]
            )
            row = account_manager.find()
            if row is None:
                return "Error: Account not found."

            # Assuming that the balance is stored in the third column of the row.
            balance = row[2]
            return f"AB {balance}"
        except Exception as ex:
            logging.error(f"Error retrieving account balance: {ex}")
            return "Error retrieving account balance."

    def handle_account_remove(self, parts: list) -> str:
        """
        Handle the AR command to remove an account.
        Expected format: AR account_number/ip_address
        """
        # Check that the command has exactly 2 parts
        if len(parts) != 2:
            return ("Error: AR command requires parameter: AR account_number/ip_address")

        # Parse the account string using the helper method.
        valid, account_info = self.parse_account_number(parts[1])
        if not valid:
            return ("Error: Invalid account string format. Expected format: number/ip_address")

        try:
            # Instantiate AccountManager with the provided account information.
            manager = AccountManager(
                bank_code=account_info["bank_code"],
                account_number=account_info["account_number"]
            )
            # Assume AccountManager defines a delete method to remove an account.
            if self.handle_account_balance(account_info["bank_code"], account_info["account_number"]) == 0:
                manager.delete()
                logging.info("Account removed: %s", account_info)
                return "AR"
            else:
                return "Error: Account balance is not 0 present could not delete."
        except Exception as e:
            logging.exception("Error removing account")
            return "Error: Could not remove account."

    def handle_bank_amount(self, parts: list) -> str:

        return "BA "+str(AccountManager.find_balance(self.server_ip))

    def handle_bank_number(self, parts: list) -> str:

        return "BN "+ str(AccountManager.all())

    def handle_bank_code(self) -> str:
        """Return bank code information (here, the server IP)."""
        return self.server_ip


    def parse_account_number(self,account_str: str) -> Tuple[bool, Optional[dict]]:
        """
        Validate and parse an account string in the format number/ip_address.
        Returns:
            A tuple (True, data_dict) if valid, or (False, None) if not.
        """
        if not account_str or "/" not in account_str:
            return False, None

        acc_num, bank_code = account_str.split("/", 1)
        # Validate account number is 10000-99999
        if not acc_num.isdigit() or not (10000 <= int(acc_num) <= 99999):
            return False, None

        # Basic IP address format validation (e.g. "192.168.1.1")
        ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        if not re.match(ip_pattern, bank_code):
            return False, None

        return True, {"account_number": acc_num, "bank_code": bank_code}

    # --- Client Handling ---

    def handle_client(self, client_socket):
        client_socket.settimeout(self.client_timeout)
        buffer = ""
        while True:
            try:
                data = client_socket.recv(1024).decode("utf-8")
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    message = message.strip()
                    if not message:
                        continue
                    logging.info(f"Received: {message}")

                    parts = message.split()
                    command = parts[0].upper()

                    handler = self.command_handlers.get(command)
                    if handler is None:
                        response = ("Error: Unknown command. Type HELP for a list "
                                    "of commands.")
                    else:
                        try:
                            response = handler(parts)
                        except Exception as e:
                            logging.error(f"Error handling command {command}: {e}")
                            response = "Error processing command."
                    client_socket.send((response + "\n").encode("utf-8"))
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

                # Close the client socket in the parent process
                client_socket.close()
        except KeyboardInterrupt:
            logging.error("Server interrupted by KeyboardInterrupt.")
        finally:
            self.server_socket.close()
            logging.info("Server shut down.")
