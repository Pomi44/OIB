import hashlib
import json
import logging

logging.basicConfig(level=logging.INFO)

def generate_card_number(bin_code: str, last_four: str, middle: int) -> str:
    """Generate a card number based on BIN code, last four digits, and middle part."""
    return f"{bin_code}{middle:06d}{last_four}"

def hash_card_number(card_number: str) -> str:
    """Hash a card number using SHA3-256 algorithm."""
    return hashlib.sha3_256(card_number.encode()).hexdigest()

def serialize_card_number(card_number: str, path: str) -> None:
    """Serialize a card number to a JSON file."""
    try:
        with open(path, 'w') as f:
            json.dump({"card_number": card_number}, f)
    except Exception as e:
        logging.error(f"An error occurred while serializing card number: {e}")

def load_config(filename):
    """Load configuration from a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)