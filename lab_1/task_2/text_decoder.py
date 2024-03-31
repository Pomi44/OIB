import os
import json
import logging

logging.basicConfig(level=logging.INFO)

def decode_text(input_path:str, output_path:str, key_path:str) -> None:
    """
    Decode encoded text in the input file using a provided key mapping.

    Parameters:
    - input_path (str): The path to the input file containing the text with encoded letters.
    - output_path (str): The path to the output file where the decoded text will be saved.
    - key_path (str): The path to the JSON file containing the key mapping for letter replacement.

    Returns:
    - None
    """
    
    try:
        with open(key_path, 'r', encoding='utf-8') as key_file:
            key_mapping = json.load(key_file)

        # Чтение текста из входного файла
        with open(input_path, 'r', encoding='utf-8') as input_file:
            input_text = input_file.read()

        # Замена символов в соответствии с ключом
        output_text = ''.join(key_mapping.get(char, char) for char in input_text)

        # Запись результата в выходной файл
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(output_text)

    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in key file: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during file processing: {e}")


if __name__ == '__main__':
    with open(os.path.join("lab_1","task_2","config2.json"), 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)
    decode_text(config["input_file"], config["output_file"], config["key2"])