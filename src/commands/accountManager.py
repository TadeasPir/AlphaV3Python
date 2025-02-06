import logging
from socket import socket

from mysql.connector import Error

import logging

from mysql.connector import Error

from src.database.database import Database

class AccountManager:
    """
    AccountManager connects to the MySQL database using the Database class and
    creates new bank accounts.
    """

    def __init__(self, bank_code,acc_number,balance=0):
        self.acc_number = acc_number
        self.bank_code = bank_code
        self.balance = balance

    def save(self):

        try:
            cursor = Database.get_cursor()

            if self.acc_number < 10000 or self.acc_number > 99999:
                logging.error("Account number must be between 10000 and 99999")
                raise ValueError("Account number must be between 10000 and 99999")


            # Insert
            query = """
                INSERT INTO Accounts (acc_number, bank_code,balance)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (self.acc_number, self.bank_code, self.balance))
            self.acc_number = cursor.lastrowid

            Database.get_connection().commit()
            cursor.close()
            logging.info(f"User saved: {self}")
        except Error as e:
            logging.error(f"Error saving user: {e}")

    def update(self):
        try:
            cursor = Database.get_cursor()

            if self.acc_number < 10000 or self.acc_number > 99999:
                logging.error("Account number must be between 10000 and 99999")
                raise ValueError("Account number must be between 10000 and 99999")


            query = """
                      UPDATE Accounts
                      SET acc_number = %s, bank_code = %s, balance = %s
                      WHERE acc_number = %s
                  """
            cursor.execute(query, (self.acc_number, self.bank_code, self.balance))


            Database.get_connection().commit()
            cursor.close()
            logging.info(f"User updated: {self}")
        except Error as e:
            logging.error(f"Error saving user: {e}")

    def delete(self):

        if not self.acc_number:
            raise ValueError("Cannot delete a user without a acc_number.")

        try:
            cursor = Database.get_cursor()
            query = "DELETE FROM Accounts WHERE acc_number = %s"
            cursor.execute(query, (self.acc_number,))
            Database.get_connection().commit()
            cursor.close()
            logging.info(f"User deleted: {self}")
        except Error as e:
            logging.error(f"Error deleting user: {e}")
            raise


    def find(self):

        try:
            cursor = Database.get_cursor()
            query = "SELECT * FROM Accounts WHERE acc_number = %s"
            cursor.execute(query, (self.acc_number,))
            row = cursor.fetchone()
            cursor.close()

            return row
        except Error as e:
            logging.error(f"Error finding user: {e}")


    @classmethod
    def all(cls):

        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT * FROM Accounts"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [cls(**row) for row in rows]
        except Error as e:
            logging.error(f"Error retrieving all Accounts: {e}")
            raise



