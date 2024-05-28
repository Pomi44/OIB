import hashlib
import json
import multiprocessing




def hash_card_number(card_number):
    return hashlib.sha256(card_number.encode()).hexdigest()

def generate_card_numbers_recursive(prefix, suffix, middle_length, current=''):
    if middle_length == 0:
        yield prefix + current + suffix
    else:
        for digit in '0123456789':
            yield from generate_card_numbers_recursive(prefix, suffix, middle_length - 1, current + digit)

def generate_card_numbers(bin, last4):
    prefix = f"{bin:06}"
    suffix = f"{last4:04}"
    yield from generate_card_numbers_recursive(prefix, suffix, 6)

def serialize_card_number(card_number, filename="card_number.json"):
    with open(filename, 'w') as f:
        json.dump({"card_number": card_number}, f)

def find_card_number(args):
    card_number, target_hash = args
    if hash_card_number(card_number) == target_hash:
        return card_number
    return None

def search_card_number(bin, last4, target_hash, process_count):
    with multiprocessing.Pool(process_count) as pool:
        card_numbers = generate_card_numbers(bin, last4)
        for card_number in pool.imap_unordered(find_card_number, ((cn, target_hash) for cn in card_numbers)):
            if card_number is not None:
                pool.terminate()
                return card_number
    return None

def get_cpu_count():
    return multiprocessing.cpu_count()
