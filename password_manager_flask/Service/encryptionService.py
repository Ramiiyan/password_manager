from app import json
from cryptography.fernet import Fernet


def encrypt_data(encrypt_key, h1, h2, m_key, crypto_data):
    mkey_s1_h1 = h1.encode(m_key, salt=encrypt_key.salt_1)
    p_hash = h1.decode(mkey_s1_h1)['hash']
    salt2 = encrypt_key.salt_2
    data_crypto_encode = h2.encode(p_hash, salt=salt2)
    data_crypto_key = h2.decode(data_crypto_encode)['hash']
    f_data = Fernet(bytes(data_crypto_key, 'utf-8'))
    encrypted_crypto_data = f_data.encrypt(bytes(crypto_data, 'utf-8'))
    return encrypted_crypto_data


def retrieve_decrypted_data(h1, h2, m_key, salt1, salt2, encrypted_json_data):
    mkey_h1_s1 = h1.encode(m_key, salt=salt1)
    p_hash_2 = h1.decode(mkey_h1_s1)['hash']
    data_crypto_encode = h2.encode(p_hash_2, salt=salt2)
    data_crypto_key = h2.decode(data_crypto_encode)['hash']
    f_data = Fernet(bytes(data_crypto_key, 'utf-8'))
    data = []
    for i in encrypted_json_data:
        each_data = i['encrypted_data']
        crypto_data = f_data.decrypt(bytes(each_data, 'utf-8'))
        print(f"Retrieved Data: {crypto_data}")
        data.append(crypto_data.decode('utf-8'))

    return data
