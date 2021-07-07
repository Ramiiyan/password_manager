import base64
import hashlib
import secrets


class HashMaker:
    algorithm = "pbkdf2_sha256"
    iterations = 260000

    def __init__(self, iterations=260000):
        self.iterations = iterations

    def encode(self, password, salt=None, iterations=None):
        if salt is None:
            salt = secrets.token_hex(16)
        assert salt and isinstance(salt, str) and "$" not in salt
        assert isinstance(password, str)
        iterations = iterations or self.iterations
        pw_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations)
        b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()
        return "{}${}${}${}".format(self.algorithm, iterations, salt, b64_hash)

    def decode(self, encoded):
        algorithm, iterations, salt, hash_1 = encoded.split('$', 3)
        assert algorithm == self.algorithm
        return {
            'algorithm': algorithm,
            'hash': hash_1,
            'iterations': int(iterations),
            'salt': salt,
        }

    def verify_password(self, password, encoded):
        decoded = self.decode(encoded)
        compare_hash = self.encode(password, decoded['salt'], decoded['iterations'])
        return secrets.compare_digest(encoded, compare_hash)
