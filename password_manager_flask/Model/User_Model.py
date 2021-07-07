from app import db, ma, json, bcrypt


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    username = db.Column(db.String(40), unique=False, nullable=True)
    password = db.Column(db.Text, unique=False, nullable=False)
    encrypt_key = db.relationship('EncryptKey', backref='user', uselist=False,
                                  cascade='all, delete-orphan')  # ( One to One)
    crypto_data = db.relationship('CryptoData', backref='user',
                                  cascade='all, delete-orphan')  # (One to Many)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def json_to_obj(cls, user_json):
        return cls(**user_json)

    def __repr__(self):
        return f'<User email: {self.email}>'
