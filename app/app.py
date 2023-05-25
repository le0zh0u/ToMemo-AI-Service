from flask import Flask, request, jsonify, make_response
from dotenv import find_dotenv, load_dotenv
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
import os
from db.db import connect_to_mysql, mysql
from utils.json_util import CustomJSONEncoder
from utils.apple_store_kit import get_request_token

from controller.user_controller import user_controller
from controller.gpt_controller import gpt_controller
from controller.apple_transaction_controller import trans_controller
from controller.license_key_admin_controller import license_key_admin_controller
from controller.license_key_controller import license_key_controller
from controller.jwt_controller import jwt_controller

from models.apple_transaction_log_model import AppleTransactionLog

app = Flask(__name__)
jwt = JWTManager(app)

app.register_blueprint(user_controller)
app.register_blueprint(gpt_controller)
app.register_blueprint(trans_controller)
app.register_blueprint(license_key_admin_controller)
app.register_blueprint(license_key_controller)
app.register_blueprint(jwt_controller)

load_dotenv(find_dotenv()) # 从 .env 文件中加载环境变量

app.config['JWT_SECRET_KEY'] = 'super-secret'  # 更改为您自己的密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)  # 设置访问令牌的到期时间

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

app.config['JSON_AS_ASCII'] = False

# 配置限流参数
app.config["RATELIMIT_HEADERS_ENABLED"] = True
app.config["RATELIMIT_STORAGE_URL"] = "memory://"
app.config["RATELIMIT_DEFAULT"] = "10/minute"  # 每分钟最多允许 10 个请求

# 创建 Limiter 实例
limiter = Limiter(key_func=get_remote_address, app=app)

# init db
connect_to_mysql(app)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(Exception)
def handle_error(error):
    # 处理异常并返回响应
    print(error)
    return make_response(jsonify({"success":-1, "message":'{}'.format(error)}), 500)

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