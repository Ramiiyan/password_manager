from flask import Flask, request, json, jsonify
import HashMaker
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet, InvalidToken
from flask_marshmallow import Marshmallow
import Service.deepHashService as dh
import Service.encryptionService as es
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# app.config['JWT_SECRET_KEY'] = config['jwt_token']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/atlas_labs'


db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

from Model.User_Model import User
from Model.Encrypt_Key_Model import EncryptKey, EncryptKeySchema
from Model.Crypto_Data_Model import CryptoData, CryptoDataSchema

h1 = HashMaker.HashMaker()
h2 = HashMaker.HashMaker()


@app.route('/')
def hello_world():
    db.create_all()
    db.session.commit()
    return "Working"


# Register New User
@app.route('/user/register', methods=['POST'])
def user_register():
    r_data = {
        "email": "tester@gmail.com",
        "username": "tester",
        "password": "password123"
    }
    user = User.json_to_obj(request.get_json())
    exist_user = User.query.filter(User.email == user.email).first()
    if not exist_user:
        db.session.add(user)
        db.session.commit()
        generate_master = generate_mkey(user.user_id)
        response = "success"
        results = {
            'email': user.email,
            'user_id': user.user_id,
            'message': 'user registered successfully',
            'generated': generate_master,


        }
    else:
        response = "error"
        results = {
            'message': "email already exists"
        }
    return jsonify({
            'response': response,
            'results': results
    })


# User Login
@app.route('/user/login', methods=['POST'])
def user_login():
    email = request.get_json()['email']
    password = request.get_json()['password']

    login = User.query.filter(User.email == email).first()
    if login:
        if bcrypt.check_password_hash(login.password, password):
            response = jsonify({
                "response": "success",
                "user_id": login.user_id
            })
        else:
            response = jsonify({
                "response": "error",
                "error": "Invalid Password."
            })
    else:
        response = jsonify({
            "response": "error",
            "error": "user not found."
        })
    return response


# Generate Master Key, Salts
@app.route('/user/generateMasterKey/<user_id>')
def generate_mkey(user_id):

    user_master_key = secrets.token_hex(32)
    salt1 = secrets.token_hex(16)
    salt2 = secrets.token_hex(16)
    encrypted_auth2 = dh.deep_hash_auth_init(h1, user_master_key, salt1)
    encrypt_key = EncryptKey(salt_1=salt1, salt_2=salt2, user_id=user_id,
                             encrypted_auth2=encrypted_auth2)
    print(encrypt_key)
    db.session.add(encrypt_key)
    db.session.commit()
    print(user_master_key)

    return {
        "master_key": user_master_key
    }


@app.route('/validate_mkey', methods=['POST'])
def validate_mkey():
    r_data = {
        "user_id": 7,
        "m_key": "myMasterKey"
    }
    print(f'Raw data: {request.get_json()}')
    user_id = request.get_json()["user_id"]
    m_key = request.get_json()["m_key"]

    encryption_keys = EncryptKey.query.filter_by(user_id=user_id).first()
    salt1 = encryption_keys.salt_1
    encrypted_auth2 = encryption_keys.encrypted_auth2
    print("salt1:" + salt1)
    print("encrypted_auth2:" + encrypted_auth2)
    validation = dh.encrypted_auth_validate(h1, m_key, salt1, encrypted_auth2)
    print(validation)
    if validation:
        # retrieve data
        salt2 = encryption_keys.salt_2
        encrypted_crypto_data = CryptoData.query.filter_by(user_id=user_id).all()
        enc_json_data = CryptoDataSchema(many=True).dump(encrypted_crypto_data)
        crypto_data = es.retrieve_decrypted_data(h1, h2, m_key, salt1, salt2, enc_json_data)
        data_msg = {
            "dataList": crypto_data
        }
    else:
        data_msg = {
            "message": "Invalid Master Key"
        }

    return jsonify({
        "response": "success",
        "validation": validation,
        "data_msg": data_msg
    })


# add encrypted_data
@app.route('/add/crypto_data', methods=['POST'])
def add_encrypted_data():
    r_data = {
        "crypto_data": "encrypted_data_from_CryptoJs",
        "m_key": "mysecretmasterkey",
        "user_id": 1
    }
    crypto_data = request.get_json()["crypto_data"]
    user_id = request.get_json()["user_id"]
    m_key = request.get_json()["m_key"]
    encrypt_key = EncryptKey.query.filter_by(user_id=user_id).first()

    encrypted_crypto_data = es.encrypt_data(encrypt_key, h1, h2, m_key, crypto_data)
    crypto = CryptoData(encrypted_data=encrypted_crypto_data, user_id=user_id)
    db.session.add(crypto)
    db.session.commit()

    return jsonify({
        "response": "success",
        "message": "data added."
    })

