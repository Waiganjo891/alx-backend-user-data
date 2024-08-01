#!/usr/bin/env python3
"""
A function called filter_datum that returns
the log message obfuscated
"""
import re
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
