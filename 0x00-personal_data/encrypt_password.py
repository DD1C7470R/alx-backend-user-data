#!/usr/bin/env python3
"""Handles password hashing"""
import bcrypt


def hash_password(password: str) -> str:
    """Handles password hashing"""
    encoded_password = password.encode('utf-8')
    return bcrypt.hashpw(encoded_password, bcrypt.gensalt())


def is_valid(hashed: bytes, password: str) -> bool:
    """Handles password unhashing"""
    if bcrypt.checkpw(password.encode('utf-8'), hashed):
        return True
    else:
        return False
