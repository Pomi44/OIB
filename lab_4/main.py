import json
import argparse
import logging

from generate_card import serialize_card_number, get_cpu_count, search_card_number

logging.basicConfig(level=logging.INFO)

def load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Card Number Search Tool")
    parser.add_argument('mode', choices=['generate'], help='Mode of operation')
    parser.add_argument('--config', type=str, help='Path to the config JSON file', required=True)
    args = parser.parse_args()

    config = load_config(args.config)

    match args.mode:
        case 'generate':
            try:
                for bin_code in config['bins']:
                    card_number = search_card_number(config['hash'], bin_code, config['last_numbers'], get_cpu_count())
                    if card_number:
                        serialize_card_number(card_number, config['data_path'])
                        logging.info(f"Found card number: {card_number}")
                        break
                else:
                    logging.info("Card number not found.")
            except Exception as e:
                logging.error(f"An error occurred in 'find' mode: {e}")

if __name__ == "__main__":
    main()
