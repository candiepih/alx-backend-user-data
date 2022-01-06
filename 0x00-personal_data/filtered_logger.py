#!/usr/bin/env python3
"""
This module contains the filter logging methods.
"""
import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filter strings representing all fields to obfuscate"""
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
            """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Return a logger with a redacting formatter"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a connection to the database"""
    db_conn = mysql.connector.connect(
        host=os.environ.get('PERSONAL_DATA_DB_HOST'),
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME'),
        passwd=os.environ.get('PERSONAL_DATA_DB_PASSWORD'),
        database=os.environ.get('PERSONAL_DATA_DB_NAME')
    )
    return db_conn


def main() -> None:
    """Fetches and returns rows in users table"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    logger = get_logger()
    fields = [field[0] for field in cursor.description]
    for row in cursor:
        str_row = "".join("{}={}; ".format(k, v)
                          for k, v in zip(fields, row))
        logger.info(str_row.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
