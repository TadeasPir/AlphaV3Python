import logging
from socket import socket
import re

from mysql.connector import Error

import logging

from mysql.connector import Error

from src.database.database import Database

class AccountManager:
    """
    AccountManager connects to the MySQL database using the Database class and
    creates new bank accounts.
    """

    def __init__(self, bank_code,account_number,balance=0):
        self.account_number = account_number
        self.bank_code = bank_code
        self.balance = balance

    def save(self):
        try:
            cursor = Database.get_cursor()

            # Insert without account_number since it's auto-generated
            query = """
                INSERT INTO Accounts (bank_code, balance)
                VALUES (%s, %s)
            """
            cursor.execute(query, (self.bank_code, self.balance))
            self.account_number = cursor.lastrowid

            Database.get_connection().commit()
            cursor.close()
            logging.info(f"User saved: {self}")

            return self.account_number

        except Error as e:
            logging.error(f"Error saving account: {e}")
            return None

    def update(self):
        try:
            cursor = Database.get_cursor()

            if int(self.account_number) < 10000 or int(self.account_number) > 99999:
                logging.error("Account number must be between 10000 and 99999")
                raise ValueError("Account number must be between 10000 and 99999")


            query = """
                      UPDATE Accounts
                      SET account_number = %s, bank_code = %s, balance = %s
                      WHERE account_number = %s
                  """
            cursor.execute(query, (self.account_number, self.bank_code, self.balance, self.account_number))


            Database.get_connection().commit()
            cursor.close()
            logging.info(f"User updated: {self}")
        except Error as e:
            logging.error(f"Error updating account: {e}")

    def delete(self):

        if not self.account_number:
            raise ValueError("Cannot delete a user without a account_number.")

        try:
            cursor = Database.get_cursor()
            query = "DELETE FROM Accounts WHERE account_number = %s"
            cursor.execute(query, (self.account_number,))
            Database.get_connection().commit()
            cursor.close()
            logging.info(f"User deleted: {self}")
        except Error as e:
            logging.error(f"Error deleting account: {e}")
            raise


    def find(self):

        try:
            cursor = Database.get_cursor()
            query = "SELECT * FROM Accounts WHERE account_number = %s"
            cursor.execute(query, (self.account_number,))
            row = cursor.fetchone()
            cursor.close()

            return row
        except Error as e:
            logging.error(f"Error finding account: {e}")

    @classmethod
    def find_balance(cls, bc):
        try:
            cursor = Database.get_cursor()
            query = ("SELECT SUM(balance) AS total_balance FROM Accounts "
                     "WHERE bank_code = %s")
            cursor.execute(query, (bc,))
            row = cursor.fetchone()
            cursor.close()

            if row is None or row[0] is None:
                return "0"
            # row[0] is expected to be a Decimal or numeric type.
            return str(row[0])
        except Error as e:
            logging.error(f"Error finding balance: {e}")
            return "Error"

    @classmethod
    def all(cls):

        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT count(*) FROM Accounts"
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            count = int(row['count(*)'])
            return count
        except Error as e:
            logging.error(f"Error retrieving all Accounts: {e}")
            raise



