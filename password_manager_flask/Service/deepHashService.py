from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet, InvalidToken


def deep_hash_auth_init(h1, m_key, salt1):
    mkey_s1_h1 = h1.encode(m_key, salt1)
    print(mkey_s1_h1)
    auth1 = h1.decode(mkey_s1_h1)['hash']   # 1st encoded hash
    print(f'auth1 ={auth1}')

    mkey_auth = h1.encode(auth1, salt1)
    print("encoded current key :" + mkey_auth)
    auth2 = h1.decode(mkey_auth)['hash']  # 2nd encoded hash
    print(f'auth2 ={auth2}')

    f = Fernet(bytes(auth1, 'utf-8'))
    encrypted_auth2 = f.encrypt(bytes(auth2, 'utf-8'))  # store
    return encrypted_auth2


def encrypted_auth_validate(h1, m_key, salt1, encrypted_auth2):
    check_auth1 = h1.encode(m_key, salt1)
    print(check_auth1)
    auth1 = h1.decode(check_auth1)['hash']  # 1st encoded hash
    print(f'auth1 ={auth1}')
    auth1_verify = h1.verify_password(m_key, check_auth1)
    print(f"Deep auth 1st Verification :{auth1_verify}")
    if auth1_verify:
        mkey_auth = h1.encode(auth1, salt1)
        auth2 = h1.decode(mkey_auth)['hash']  # 2nd encoded hash
        print(f'auth2 ={auth2}')
        auth2_verify = h1.verify_password(auth1, mkey_auth)
        print(f"Deep auth 2nd Verification :{auth2_verify}")
        if auth2_verify:
            try:
                f = Fernet(bytes(auth1, 'utf-8'))
                b_auth2 = f.decrypt(bytes(encrypted_auth2, 'utf-8'))
                print(b_auth2)
                print(bytes(auth2, 'utf-8'))
            except InvalidSignature:
                print("Invalid Master Key")
                return False
            except InvalidToken:
                print("Invalid Token (auth_1)")
                return False

            if b_auth2 == bytes(auth2, 'utf-8'):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


