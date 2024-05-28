import argparse
import logging

from card_utils import serialize_card_number, load_config
from search import find_card_number_parallel, get_cpu_count


logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="Card Number Search Tool")
    parser.add_argument('mode', choices=['generate'], help='Mode of operation')
    parser.add_argument('--config', type=str, help='Path to the config JSON file', required=True)
    args = parser.parse_args()

    config = load_config(args.config)

    if args.mode == 'generate':
        try:
            process_count = get_cpu_count()
            for bin_code in config['bins']:
                logging.info(f"Searching card number with BIN: {bin_code}")
                card_number = find_card_number_parallel(config['hash'], str(bin_code), config['last_numbers'], process_count)
                if card_number:
                    serialize_card_number(card_number, config['data_path'])
                    logging.info(f"Found card number: {card_number}")
                    break
            else:
                logging.info("Card number not found.")
        except Exception as e:
            logging.error(f"An error occurred in 'generate' mode: {e}")

if __name__ == "__main__":
    main()