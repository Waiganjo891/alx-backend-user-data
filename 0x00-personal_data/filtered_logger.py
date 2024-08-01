#!/usr/bin/env python3
"""
A function called filter_datum that returns
the log message obfuscated.
"""
import re
import logging
from typing import List


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Obfuscate specified fields in the log message.
    :param fields: List of fields to obfuscate.
    :param redaction: String used to replace field values.
    :param message: The log message containing fields and values.
    :param separator: Character separating the fields in the log message.
    :return: The obfuscated log message.
    """
    return re.sub(
        '|'.join(
            [f"(?<={field}{separator})[^\\{separator}]*" for field in fields]
            ),
        redaction,
        message
    )


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to redact.
        :param fields: List of field names to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating sensitive fields.
        :param record: The log record.
        :return: The formatted and obfuscated log message.
        """
        record.msg = filter_datum(
                            self.fields,
                            self.REDACTION,
                            record.msg,
                            self.SEPARATOR
                            )
        return super().format(record)
