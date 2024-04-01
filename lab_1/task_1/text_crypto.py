from w_r_files import *


def caesar_cipher_key(shift: int, alphabet_filename: str, output_filename: str) -> dict:
    """
    Generates a key for the Caesar cipher with a given shift and writes it to a file.

    Parameters:
        shift: The numerical shift for the Caesar cipher.
        alphabet_filename: The name of the file containing the Russian alphabet.
        output_filename: The name of the file to write the key to.

    Returns:
        dict: A dictionary representing the Caesar cipher encryption key.
    """
    try:
        russian_alphabet = read_txt_file(alphabet_filename)

        shifted_alphabet = russian_alphabet[shift:] + russian_alphabet[:shift]
        key = {russian_alphabet[i]: shifted_alphabet[i] for i in range(len(russian_alphabet))}
        
        write_json_file(output_filename, key)

        return key
    except Exception as e:
        print(f"Error generating key: {e}")


def encrypt_with_key(text: str, key_filename: str, output_filename: str,decrypt: bool = False) -> str:
    """
    Encrypts the text using the key from the JSON file and writes the result to a file.

    Parameters:
        text: The original text to encrypt.
        key_filename: The filename of the JSON file containing the encryption key.
        output_filename: The name of the file to write the encrypted text to.

    Returns:
        str: The encrypted text.
    """
    try:
        key = read_json_file(key_filename)
        if decrypt:
            key = {v: k for k, v in key.items()}
        encrypted_text = ''.join(key.get(char, char) for char in text)
        write_txt_file(output_filename, encrypted_text)
        return encrypted_text
    except Exception as e:
        print(f"Error encrypting text: {e}")


if __name__ == '__main__':
    try:
        config = read_json_file("config1.json")

        text_filename = config["text_filename"]
        text = read_txt_file(text_filename)

        alphabet = config["alphabet_filename"]
        shift = config["shift"]
        key = config["key_filename"]
        caesar_cipher_key(shift, alphabet, key)

        encrypted_text_filename = config["encrypted_text_filename"]
        decrypt = config["decrypt"]
        encrypted_text = encrypt_with_key(text, key, encrypted_text_filename, decrypt)
        
    except Exception as e:
        print(f"An error occurred: {e}")