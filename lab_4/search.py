import logging
import multiprocessing as mp

from tqdm import tqdm
from card_utils import generate_card_number, hash_card_number


logging.basicConfig(level=logging.INFO)


def find_card_number(hash_target: str, bin_code: str, last_four: str, middle_range: range) -> str:
    """Find a card number that matches the given hash target within the specified range of middle parts."""
    try:
        for middle in middle_range:
            card_number = generate_card_number(bin_code, last_four, middle)
            if hash_card_number(card_number) == hash_target:
                return card_number
        return None
    except Exception as e:
        logging.error(f"An error occurred while finding card number: {e}")
        return None

def find_card_number_parallel(hash_target: str, bin_code: str, last_four: str, process_count: int) -> str:
    """Find a card number in parallel using multiple processes."""
    try:
        pool = mp.Pool(process_count)
        chunk_size = 1000000 // process_count
        ranges = [(hash_target, bin_code, last_four, range(i * chunk_size, (i + 1) * chunk_size)) for i in range(process_count)]
        with tqdm(total=1000000, desc="Searching") as pbar:
            results = pool.starmap(find_card_number, ranges)
            for result in results:
                pbar.update(chunk_size)
                if result:
                    pool.terminate()
                    return result
        return None
    except Exception as e:
        logging.error(f"An error occurred while finding card number in parallel: {e}")
        return None

def get_cpu_count() -> int:
    """Get the number of available CPU cores."""
    try:
        return mp.cpu_count()
    except Exception as e:
        logging.error(f"An error occurred while getting CPU count: {e}")