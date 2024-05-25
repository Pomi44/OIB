import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

logging.basicConfig(level=logging.INFO)

class EncryptionHelper:
    """
    Utility class providing helper methods for encryption, decryption, and file I/O.
    """

    @staticmethod
    def serialize_key(key, key_path: str, key_type: str) -> None:
        """
        Serialize a key to a file.

        Args:
            key: The key object to be serialized (public or private key).
            key_path (str): The path to save the serialized key.
            key_type (str): The type of the key ('public' or 'private').
        """
        try:
            with open(key_path, 'wb') as key_file:
                if key_type == 'public':
                    key_bytes = key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    )
                elif key_type == 'private':
                    key_bytes = key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()
                    )
                else:
                    raise ValueError("Invalid key type. Must be 'public' or 'private'.")

                key_file.write(key_bytes)
        except Exception as e:
            logging.error(f"Failed to serialize {key_type} key: {e}")

    @staticmethod
    def load_key_from_file(key_file_path: str) -> rsa.RSAPublicKey:
        """
        Deserialize a key from a file.

        Args:
            key_file_path (str): The path to the file containing the serialized key.
            is_public (bool): Indicates whether the key to be loaded is public or private.

        Returns:
            rsa.RSAPublicKey: The deserialized RSA key.
        """

        
        try:
            with open(key_file_path, "rb") as private_key_file:
                    return serialization.load_pem_private_key(
                        private_key_file.read(),
                        password=None
                    )
        except Exception as e:
            logging.error(f"Failed to deserialize private key: {e}")

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