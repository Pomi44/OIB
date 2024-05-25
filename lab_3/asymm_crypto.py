import logging
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

logging.basicConfig(level=logging.INFO)

class AsymmCrypt:
    """
    Provides methods for asymmetric encryption and decryption using RSA algorithm.
    """

    def generate_key_pair(self) -> tuple:
        """
        Generates a pair of RSA private and public keys.

        Returns:
            tuple: A tuple containing RSA private key and public key.
        """
        try:
            keys = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            private_key = keys
            public_key = keys.public_key()
            logging.info("RSA key pair generated successfully.")
            return private_key, public_key
        except Exception as e:
            logging.error(f"Failed to generate key pair: {e}")
            raise

    def encrypt_with_public_key(self, public_key: rsa.RSAPublicKey, text) -> bytes:
        """
        Encrypts text with the provided RSA public key.

        Args:
            public_key: RSA public key used for encryption.
            text (bytes): Text to be encrypted.

        Returns:
            bytes: Encrypted text.
        """
        try:
            encrypted_text = public_key.encrypt(
                text,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            logging.info("Text encrypted successfully.")
            return encrypted_text
        except Exception as e:
            logging.error(f"Failed to encrypt with public key: {e}")
            raise

    def decrypt_with_private_key(self, private_key: rsa.RSAPrivateKey, encrypted_text: bytes) -> bytes:
        """
        Decrypts encrypted text with the provided RSA private key.

        Args:
            private_key: RSA private key used for decryption.
            encrypted_text (bytes): Encrypted text to be decrypted.

        Returns:
            bytes: Decrypted text.
        """
        try:
            decrypted_text = private_key.decrypt(
                encrypted_text,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            logging.info("Text decrypted successfully.")
            return decrypted_text
        except Exception as e:
            logging.error(f"Failed to decrypt with private key: {e}")
            raise
