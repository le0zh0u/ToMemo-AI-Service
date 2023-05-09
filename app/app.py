from flask import Flask, request, jsonify
from dotenv import find_dotenv, load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import openai
import os
import random

from controller.user_controller import user_controller
from controller.gpt_controller import gpt_controller

app = Flask(__name__)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # 更改为您自己的密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)  # 设置访问令牌的到期时间

load_dotenv(find_dotenv()) # 从 .env 文件中加载环境变量

app.register_blueprint(user_controller)
app.register_blueprint(gpt_controller)

@app.errorhandler(Exception)
def handle_error(error):
    # 处理异常并返回响应
    return jsonify({"success":-1, "message":'{}'.format(error)}), 500


@app.route("/")
def hello_world():
    return jsonify({"key":os.environ.get("OPENAI_API_KEY")})

if __name__ == '__main__':
    app.run()