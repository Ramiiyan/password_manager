from cryptography.fernet import Fernet

auth1 = 'EZzYlvrLDfLBzyW9Vsf3KNrPT2hOUhF96M7TUmtgjBo='
auth2 = 'q5KsFRf0NSUOHgDQyBrkw7I3RtSVzOcLeOgunMTo+vE='
f = Fernet
f1 = f(bytes(auth1, 'utf-8'))
encrypted_auth2 = f1.encrypt(bytes(auth2, 'utf-8'))
print(encrypted_auth2)
b_auth = f1.decrypt(encrypted_auth2)
print(b_auth == bytes(auth2, 'utf-8'))
