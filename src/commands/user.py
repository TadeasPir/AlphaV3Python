import csv
import logging
from mysql.connector import Error
from src.database.database import Database

class User:
    def __init__(self, user_id=None, username=None, email=None, is_active=True, credit_points=0.0):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.is_active = is_active
        self.credit_points = credit_points

    def save(self):

        try:
            cursor = Database.get_cursor()
            if self.user_id:
                # Update
                query = """
                    UPDATE Users
                    SET username = %s, email = %s, is_active = %s, credit_points = %s
                    WHERE user_id = %s
                """
                cursor.execute(query, (self.username, self.email, self.is_active, self.credit_points, self.user_id))
            else:
                # Insert
                query = """
                    INSERT INTO Users (username, email, is_active, credit_points)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (self.username, self.email, self.is_active, self.credit_points))
                self.user_id = cursor.lastrowid

            Database.get_connection().commit()
            cursor.close()
            logging.info(f"User saved: {self}")
        except Error as e:
            logging.error(f"Error saving user: {e}")



    def delete(self):

        if not self.user_id:
            raise ValueError("Cannot delete a user without a user_id.")

        try:
            cursor = Database.get_cursor()
            query = "DELETE FROM Users WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            Database.get_connection().commit()
            cursor.close()
            logging.info(f"User deleted: {self}")
        except Error as e:
            logging.error(f"Error deleting user: {e}")
            raise


    def find(self):

        try:
            cursor = Database.get_cursor()
            query = "SELECT * FROM Users WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            row = cursor.fetchone()
            cursor.close()

            return row
        except Error as e:
            logging.error(f"Error finding user: {e}")


    @classmethod
    def all(cls):

        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT * FROM Users"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [cls(**row) for row in rows]
        except Error as e:
            logging.error(f"Error retrieving all users: {e}")
            raise



    @classmethod
    def transfer_credits(cls, from_user_id, to_user_id, amount):

        if amount <= 0:
            raise ValueError("Amount must be positive.")
            logging.error("Amount must be positive.")

        conn = Database.get_connection()
        cursor = conn.cursor()

        try:
            conn.start_transaction()

            from_user_temp = User(user_id=from_user_id).find()

            to_user_temp = User(user_id=to_user_id).find()
            from_user = User(user_id=from_user_temp[0],username=from_user_temp[1],email= from_user_temp[2], credit_points=from_user_temp[4])

            to_user = User(user_id=to_user_temp[0],username=to_user_temp[1],email= to_user_temp[2], credit_points=to_user_temp[4])




            if from_user is None or to_user is None:
                logging.error("One of the users does not exist.")


            if from_user.credit_points < amount:
                logging.error("Insufficient credit points in source user account.")



            from_user.credit_points = from_user.credit_points - amount
            to_user.credit_points = amount + to_user.credit_points


            update_query = "UPDATE Users SET credit_points = %s WHERE user_id = %s"
            cursor.execute(update_query, (from_user.credit_points, from_user.user_id))
            cursor.execute(update_query, (to_user.credit_points, to_user.user_id))

            conn.commit()
            cursor.close()
            logging.info(f"Transferred {amount} from User {from_user_id} to User {to_user_id}")

        except Error as e:
            conn.rollback()
            logging.error(f"Error transferring credits: {e}")
        finally:
                cursor.close()




    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}', " \
               f"is_active={self.is_active}, credit_points={self.credit_points})"
