import logging
from distutils.command.config import config

import mysql.connector
from mysql.connector import Error

import yaml

from config.config import Config


class Database:
    _connection = None


    @classmethod
    def _load_config(cls):
        """Load database configuration from config.yaml file"""
        try:
            config = Config("config/config.yaml")
            return config
        except Exception as e:
            logging.error(f"Failed to load database configuration: {str(e)}")


    @classmethod
    def connect(cls,config):

        if cls._connection is None:
            try:
                cls._connection = mysql.connector.connect(
                    host=config.host,
                    user=config.user,
                    password=config.password,
                    database=config.database)
                logging.info("Connected to the database successfully.")
            except Error as e:
                logging.error(f"Failed to connect to the database: {e}")
                raise

    @classmethod
    def get_connection(cls):
        config = cls._load_config()
        cls.connect(config)
        return cls._connection

    @classmethod
    def close_connection(cls):

        if cls._connection is not None and cls._connection.is_connected():
            cls._connection.close()
            cls._connection = None
            logging.info("Database connection closed.")

    @classmethod
    def get_cursor(cls, dictionary=False):

        conn = cls.get_connection()
        return conn.cursor(dictionary=dictionary)
