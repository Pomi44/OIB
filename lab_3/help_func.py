import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

logging.basicConfig(level=logging.INFO)

class EncryptionHelper:
    """
    Utility class providing helper methods for encryption, decryption, and file I/O.
    """

    @staticmethod
    def save_key_to_file(key_bytes: bytes, key_file_path: str, is_public: bool) -> None:
        """
        Serialize a key to a file.

        Args:
            key_bytes (bytes): The bytes representing the key.
            key_file_path (str): The path to save the serialized key.
            is_public (bool): Indicates whether the key is public or private.
        """
        key_type = serialization.PublicFormat.SubjectPublicKeyInfo if is_public else serialization.PrivateFormat.TraditionalOpenSSL
        key_label = "public" if is_public else "private"
        
        try:
            with open(key_file_path, "wb") as key_file:
                key_file.write(key_bytes.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=key_type
                ))
            logging.info(f"{key_label.capitalize()} key saved to {key_file_path}.")
        except Exception as e:
            logging.error(f"Failed to save {key_label} key to {key_file_path}: {e}")

    @staticmethod
    def load_key_from_file(key_file_path: str, is_public: bool) -> rsa.RSAPublicKey:
        """
        Deserialize a key from a file.

        Args:
            key_file_path (str): The path to the file containing the serialized key.
            is_public (bool): Indicates whether the key to be loaded is public or private.

        Returns:
            rsa.RSAPublicKey: The deserialized RSA key.
        """
        key_label = "public" if is_public else "private"
        
        try:
            with open(key_file_path, "rb") as key_file:
                if is_public:
                    return serialization.load_pem_public_key(
                        key_file.read(),
                    )
                else:
                    return serialization.load_pem_private_key(
                        key_file.read(),
                        password=None
                    )
            logging.info(f"{key_label.capitalize()} key loaded from {key_file_path}.")
        except Exception as e:
            logging.error(f"Failed to load {key_label} key from {key_file_path}: {e}")

    @staticmethod
    def write_to_file(file_path: str, data: bytes) -> None:
        """
        Write bytes data to a file.

        Args:
            file_path (str): The path to save the data.
            data (bytes): The bytes data.
        """
        try:
            with open(file_path, "wb") as file:
                file.write(data)
            logging.info(f"Data written to {file_path}.")
        except Exception as e:
            logging.error(f"Failed to write data to {file_path}: {e}")

    @staticmethod
    def read_from_file(file_path: str) -> bytes:
        """
        Read bytes from a file.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            bytes: The bytes read from the file.
        """
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
            logging.info(f"Data read from {file_path}.")
            return data
        except Exception as e:
            logging.error(f"Failed to read data from {file_path}: {e}")