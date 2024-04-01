import json
import os


def read_txt_file(filename: str) -> str:
    """
    Reads text from a file.

    Parameters:
        filename: The name of the file to read from.

    Returns:
        str: The read text.
    """
    try:
        with open(os.path.join("lab_1","task_1",filename), 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")


def write_txt_file(filename: str, text: str) -> None:
    """
    Writes text to a file.

    Parameters:
        filename: The name of the file to write to.
        text: The text to write to the file.
    """
    try:
        with open(os.path.join("lab_1","task_1",filename), 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Error writing to file '{filename}': {e}")


def read_json_file(filename: str) -> dict:
    """
    Reads data from a JSON file and returns a dictionary.

    Parameters:
        filename: The name of the JSON file to read from.

    Returns:
        dict: The data dictionary from the JSON file.
    """
    try:
        with open(os.path.join("lab_1","task_1",filename), 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file '{filename}'.")
    except Exception as e:
        print(f"Error reading JSON file '{filename}': {e}")


def write_json_file(filename: str, data: dict) -> None:
    """
    Writes data to a JSON file.

    Parameters:
        filename: The name of the file to write to.
        data: The data to write to the JSON file.
    """
    try:
        with open(os.path.join("lab_1","task_1",filename), 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing to JSON file '{filename}': {e}")