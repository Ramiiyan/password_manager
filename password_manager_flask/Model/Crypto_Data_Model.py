from app import db, ma, json


class CryptoData(db.Model):
    cryptoData_id = db.Column(db.Integer, primary_key=True)
    encrypted_data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                        nullable=False, unique=False)    # Unique= False -> (One to Many)

    def __init__(self, encrypted_data, user_id):
        self.encrypted_data = encrypted_data
        self.user_id = user_id

    @classmethod
    def json_to_obj(cls, crypto_json):
        return cls(**crypto_json)

    def __repr__(self):
        return f'<Pwd_list: {self.pwd_id}>'


class CryptoDataSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ("cryptoData_id", "encrypted_data", "user_id")
