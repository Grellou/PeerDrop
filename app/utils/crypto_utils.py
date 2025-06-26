from cryptography.fernet import Fernet

# File encryption
def encrypt_file(input_path, output_path):
    key = Fernet.generate_key()
    fernet = Fernet(key)

    # Read all file data
    with open(input_path, "rb") as file:
        file_data = file.read()

    # Encrypt data
    encrypted_data = fernet.encrypt(file_data)
    
    # Write encrypted data
    with open(output_path, "wb") as file:
        file.write(encrypted_data)
    return key

# File decryption
def decrypt_file(input_path, output_path, key):
    fernet = Fernet(key)

    # Read all encrypted data
    with open(input_path, "rb") as file:
        encrypted_data = file.read()

    # Decrypt data
    decrypted_data = fernet.decrypt(encrypted_data)

    # Write to original file
    with open(output_path, "wb") as file:
        file.write(decrypted_data)
