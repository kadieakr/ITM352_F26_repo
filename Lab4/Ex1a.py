from cryptography.fernet import Fernet


key = Fernet.generate_key()
cipher_suite = Fernet(key)

user_text = input("Enter a message to encrypt: ")
encoded_text = user_text.encode("utf-8")
encrypted_text = cipher_suite.encrypt(encoded_text)
decrypted_text = cipher_suite.decrypt(encrypted_text)
decoded_text = decrypted_text.decode("utf-8")

print("Encrypted text:", encrypted_text)
print("Decrypted text:", decoded_text)

