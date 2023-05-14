from flask import Flask, request, jsonify
from dotenv import find_dotenv, load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os
from db.db import connect_to_mysql, mysql
from utils.json_util import CustomJSONEncoder
from utils.apple_store_kit import get_request_token

from controller.user_controller import user_controller
from controller.gpt_controller import gpt_controller
from controller.apple_transaction_controller import trans_controller

from models.apple_transaction_log_model import AppleTransactionLog

app = Flask(__name__)
jwt = JWTManager(app)

app.register_blueprint(user_controller)
app.register_blueprint(gpt_controller)
app.register_blueprint(trans_controller)

load_dotenv(find_dotenv()) # 从 .env 文件中加载环境变量

app.config['JWT_SECRET_KEY'] = 'super-secret'  # 更改为您自己的密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)  # 设置访问令牌的到期时间

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

# init db
connect_to_mysql(app)

@app.errorhandler(Exception)
def handle_error(error):
    # 处理异常并返回响应
    return jsonify({"success":-1, "message":'{}'.format(error)}), 500

@app.route("/getAppJWT") 
def getAppJWT():
    return jsonify({"token":get_request_token()}), 200

@app.route("/")
def hello_world():
    appleTransactionList = AppleTransactionLog.query.all()
    print(appleTransactionList)
    return jsonify({"transactionList":appleTransactionList[0].transaction_id})

if __name__ == '__main__':
    app.run()