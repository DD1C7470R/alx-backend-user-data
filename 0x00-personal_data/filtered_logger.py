#!/usr/bin/env python3
"""get filtered logs"""
import logging
import re
from typing import List


pattern = r'(?<={}=).*?(?={})'


def filter_datum(
            fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(pattern.format(field, separator), redaction, message)
    return message
