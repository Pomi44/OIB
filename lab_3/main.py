import os
import json
import argparse

from asymm_crypto import AsymmCrypt
from symm_crypto import SymmCrypt
from help_func import EncryptionHelper

def main(config_path, operation):
    with open("lab_3/config.json", 'r') as f:
        config = json.load(f)
    if operation:
        config["mode"] = operation
    asymm_crypt = AsymmCrypt()
    symm_crypt = SymmCrypt(key_len=config["key_length"])
    help_func = EncryptionHelper()

    match config["mode"]:
        case 'gen':
            sym_key = symm_crypt.generate_key()
            private_key, public_key = asymm_crypt.generate_key_pair()
            encrypted_sym_key = asymm_crypt.encrypt_with_public_key(public_key, sym_key)
            help_func.write_to_file(config["symmetric_key_file"], encrypted_sym_key)
            help_func.serialize_key(private_key, config["private_key"],'private')
            help_func.serialize_key(public_key, config["public_key"],'public')

        case 'enc':
            private_key = help_func.load_key_from_file(config["private_key"])
            encrypted_sym_key = help_func.read_from_file(config["symmetric_key_file"])
            decrypted_sym_key = asymm_crypt.decrypt_with_private_key(private_key, encrypted_sym_key)
            text = help_func.read_from_file(config["text_file"])
            symm_crypt.encrypt_text(decrypted_sym_key, config["encrypted_text_file"], config["iv_path_file"], config["block_size"], text)

        case 'dec':
            private_key = help_func.load_key_from_file(config["private_key"])
            encrypted_sym_key = help_func.read_from_file(config["symmetric_key_file"])
            decrypted_sym_key = asymm_crypt.decrypt_with_private_key(private_key, encrypted_sym_key)
            symm_crypt.decrypt_text(decrypted_sym_key, config["decrypted_text_file"], config["iv_path_file"], config["encrypted_text_file"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some cryptographic operations.")
    parser.add_argument("--config_path", type=str, default= os.path.join('C','Users''ksush','OneDrive''Рабочий стол','OIB''lab_3','config.json'), help="Path to the JSON configuration file.")
    parser.add_argument("--operation", type=str, default= "dec", help="Operation to perform (overrides the operation in the config file).")
    
    args = parser.parse_args()
    main(args.config_path, args.operation)