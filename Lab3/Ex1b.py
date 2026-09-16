from cryptography.format import format

key=format.generate_key()
cypher_suite=format(key)


encoded_text=cypher_suite.encrypt(b"Hello World")
print(encoded_text)
decoded_text=cypher_suite.decrypt(encoded_text)
print(decoded_text)
