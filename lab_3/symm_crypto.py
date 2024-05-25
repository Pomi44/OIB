import os
import logging

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from help_func import EncryptionHelper

logging.basicConfig(level=logging.INFO)

class SymmCrypt:
    """
    Symmetric Cryptography class for encryption and decryption.

    Attributes:
        key (bytes): The symmetric key.
        block_size (int): The block size for the IV.
        key_sizes (frozenset): The set of allowed key sizes.

    Methods:
        generate_key(): Generates a symmetric key of specified length.
        encrypt_text(encrypted_text_path, iv_path, text): Encrypts the given text using the symmetric key and saves the encrypted text to a file.
        decrypt_text(decrypted_text_path, iv_path, ciphertext_path): Decrypts the given ciphertext using the symmetric key and saves the decrypted text to a file.
    """


    def __init__(self, key_len: int) -> None:
        """
        Initializes the SymmCrypt object with the specified key length.

        Args:
            key_len (int): The length of the symmetric key in bits.
        """
        self.key_len = key_len


    def generate_key(self) -> bytes:
        """
        Generates a symmetric key of the specified length.

        Returns:
            bytes: The generated symmetric key.
        """
        try:
            return os.urandom(self.key_len//8)
        except Exception as e:
            logging.error(f"Failed to generate key: {e}")



    def encrypt_text(self, key: bytes, encrypted_text_path: str, iv_path: str, block_size:int, text: bytes) -> None:
        """
        Encrypts the given text using the symmetric key and saves the encrypted text to a file.

        Args:
            encrypted_text_path (bytes): The path where the encrypted text will be saved.
            iv_path (str): Path to the IV text file.
            text (bytes): The text to be encrypted.
        """
        try:
            iv = os.urandom(block_size)
            cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_text = padder.update(text) + padder.finalize()
            ciphertext = iv + encryptor.update(padded_text) + encryptor.finalize()

            EncryptionHelper.write_to_file(iv_path, iv)
            EncryptionHelper.write_to_file(encrypted_text_path, ciphertext[block_size:])
        except Exception as e:
            logging.error(f"Failed to encrypt text: {e}")

    def decrypt_text(self, key:bytes, decrypted_text_path: str, iv_path: str, ciphertext_path: str) -> None:
        """
        Decrypts the given ciphertext using the symmetric key and saves the decrypted text to a file.

        Args:
            decrypted_text_path (str): The path where the decrypted text will be saved.
            iv_path (str): Path to the IV text file.
            ciphertext_path (str): The ciphertext to be decrypted.
        """
        try:
            iv = EncryptionHelper.read_from_file(iv_path)
            ciphertext = EncryptionHelper.read_from_file(ciphertext_path)

            cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(plaintext) + unpadder.finalize()

            with open(decrypted_text_path, "wb") as decrypted_text_file:
                decrypted_text_file.write(plaintext)
        except Exception as e:
            logging.error(f"Failed to decrypt text: {e}")