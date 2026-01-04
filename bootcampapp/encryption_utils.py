from cryptography.fernet import Fernet

# Key for encryption and decryption (store securely, e.g., in environment variables)
SECRET_KEY = Fernet.generate_key()  # Replace this with a key retrieved from a secure location
cipher_suite = Fernet(SECRET_KEY)

def encrypt_password(password):
    """Encrypt the password."""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    """Decrypt the password."""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()
