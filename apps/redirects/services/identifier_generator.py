# apps/redirects/services/identifier_generator.py
import string
import random
from typing import Set


class IdentifierGenerator:
    """
    Service for generating unique identifiers for redirect rules
    """
    def __init__(self, length: int = 8):
        self.length = length
        self.chars = string.ascii_letters + string.digits

    def generate(self, existing_identifiers: Set[str] = None) -> str:
        """
        Generate a unique identifier
        """
        while True:
            identifier = ''.join(random.choices(self.chars, k=self.length))
            if existing_identifiers is None or identifier not in existing_identifiers:
                return identifier
