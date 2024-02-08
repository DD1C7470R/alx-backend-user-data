#!/usr/bin/env python3
"""get filtered logs"""
import logging
import mysql.connector
import re
from typing import List


pattern = r'(?<={}=).*?(?={})'
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
            fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(pattern.format(field, separator), redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """to filter values in incoming log records using filter_datum"""
        msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a  returns a connector to the database"""
    from os import getenv
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host=getenv('PERSONAL_DATA_DB_HOST'),
            user=getenv('PERSONAL_DATA_DB_USERNAME'),
            password=getenv('PERSONAL_DATA_DB_PASSWORD'),
            database=getenv('PERSONAL_DATA_DB_NAME'),
            port=3306
        )
        return connection
    except mysql.connector.Error as err:
        return None
