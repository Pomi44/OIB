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

    name = "Blowfish"
    block_size = 64
    key_sizes = frozenset(range(32, 449, 8))

    def __init__(self, key: bytes) -> None:
        """
        Initializes the SymmCrypt object with the specified symmetric key.

        Args:
            key (bytes): The symmetric key.
        """
        self.key = self._verify_key_size(key)


    def key_size(self) -> int:
        """
        Returns the size of the symmetric key in bits.

        Returns:
            int: The size of the symmetric key in bits.
        """
        return len(self.key) * 8

    def _verify_key_size(self, key: bytes) -> bytes:
        """
        Verifies that the length of the key is within the allowed range.

        Args:
            key (bytes): The symmetric key.

        Returns:
            bytes: The symmetric key.

        Raises:
            ValueError: If the length of the key is not within the allowed range.
        """
        key_len = len(key) * 8
        if key_len not in self.key_sizes:
            raise ValueError(f"Invalid key size. Allowed key sizes: {self.key_sizes}")
        return key

    def generate_key(self) -> bytes:
        """
        Generates a symmetric key of the specified length.

        Returns:
            bytes: The generated symmetric key.
        """
        try:
            return os.urandom(self.block_size // 8)
        except Exception as e:
            logging.error(f"Failed to generate key: {e}")

    def encrypt_text(self, encrypted_text_path: str, iv_path: str, text: bytes) -> None:
        """
        Encrypts the given text using the symmetric key and saves the encrypted text to a file.

        Args:
            encrypted_text_path (bytes): The path where the encrypted text will be saved.
            iv_path (str): Path to the IV text file.
            text (bytes): The text to be encrypted.
        """
        try:
            iv = os.urandom(self.block_size // 8)
            cipher = Cipher(algorithms.Blowfish(self.key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_text = padder.update(text) + padder.finalize()
            ciphertext = iv + encryptor.update(padded_text) + encryptor.finalize()

            EncryptionHelper.write_to_file(iv_path, iv)
            EncryptionHelper.write_to_file(encrypted_text_path, ciphertext[self.block_size // 8:])
        except Exception as e:
            logging.error(f"Failed to encrypt text: {e}")

    def decrypt_text(self, decrypted_text_path: str, iv_path: str, ciphertext_path: str) -> None:
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

            cipher = Cipher(algorithms.Blowfish(self.key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(plaintext) + unpadder.finalize()

            with open(decrypted_text_path, "wb") as decrypted_text_file:
                decrypted_text_file.write(plaintext)
        except Exception as e:
            logging.error(f"Failed to decrypt text: {e}")