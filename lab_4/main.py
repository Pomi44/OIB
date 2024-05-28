import argparse
import logging

from card_utils import serialize_card_number, load_config
from search import find_card_number_parallel, get_cpu_count
from luhn_validator import luhn_check
from benchmark import measure_time, plot_time_vs_processes

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Card Number Search Tool")
    parser.add_argument('mode', choices=['generate', 'validate', 'benchmark'], help='Mode of operation')
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

    elif args.mode == 'validate':
        card_number = input("Enter the card number to validate: ")
        if luhn_check(card_number):
            logging.info("The card number is valid.")
        else:
            logging.info("The card number is invalid.")

    elif args.mode == 'benchmark':
        max_processes = int(1.5 * get_cpu_count())
        processes, times = measure_time(config['hash'], config['bins'][0], config['last_numbers'], max_processes)
        plot_time_vs_processes(processes, times)

if __name__ == "__main__":
    main()