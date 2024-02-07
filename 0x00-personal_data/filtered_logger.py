#!/usr/bin/env python3
"""get filtered logs"""
import logging
import re


pattern = r'(?<={}=).*?(?={})'


def filter_datum(fields, redaction, message, separator) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        §message = re.sub(pattern.format(field, separator), redaction, message)
    return message
