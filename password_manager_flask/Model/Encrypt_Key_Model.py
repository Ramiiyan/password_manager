from app import db, ma, json
from Model import User_Model


class EncryptKey(db.Model):
    enc_id = db.Column(db.Integer, primary_key=True)
    salt_1 = db.Column(db.String(100), nullable=False)
    salt_2 = db.Column(db.String(100), nullable=False)
    encrypted_auth2 = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                        nullable=False, unique=True)  # unique = True( One to One)

    def __init__(self, salt_1, salt_2, encrypted_auth2, user_id):
        self.salt_1 = salt_1
        self.salt_2 = salt_2
        self.encrypted_auth2 = encrypted_auth2
        self.user_id = user_id

    @classmethod
    def json_to_obj(cls, encrypt_key_json):
        return cls(**encrypt_key_json)

    def __repr__(self):
        return f'<encrypt: {self.enc_id}>'


class EncryptKeySchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ("enc_id", "salt_1", "salt_2", "user_id")
