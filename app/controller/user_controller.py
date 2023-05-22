from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity

from service.apple_uniqe_user_service import relate_unique_user_with_license_key, verify_unique_user_id_with_license_key,generate_unique_user_jwt

import os

user_controller = Blueprint('user', __name__)

# @user_controller.route('/jwt/get', method=['POST'])
# def getJWT():
#     uniqueUserId = request.json.get('uniqueUserId')
#     licenseKey = request.json.get('licenseKey')

#     if not uniqueUserId:
#         return jsonify({"successs":-1, "message":"用户唯一id为空"}), 200
#     if not licenseKey:
#         return jsonify({"successs":-1, "message":"LicenseKey为空"}), 200

#     #TODO 是否在黑名单中
    

#     # 如果用户存在，则创建 JWT access token
#     access_token = create_access_token(identity=uniqueUserId)
#     #TODO 保存jwt到数据库中 userid - jwt
#     return jsonify(access_token=access_token), 200

@user_controller.route('/user/token/generate', methods=['POST'])
def use_license_key():
    unique_user_id = request.json.get('uniqueUserId')
    license_key = request.json.get('licenseKey')

    if not unique_user_id:
        return jsonify({"success":-1, "message":"用户唯一id为空"}), 200
    
    # 进行身份验证逻辑并检查用户是否存在
    # - LicekseKey是否有效
    # - 关联关系不能多余6条（限制6台设备关联）
    # verify_result = verify_unique_user_id_with_license_key(unique_user_id, license_key)
    # if verify_result[0] == False:
    #     return jsonify({"success":-1, "message": verify_result[1]}), 200
    
    # 用户关系处理，
    # 如果关联不存在，需要创建userid和license_key的关联关系 
    rel_result = relate_unique_user_with_license_key(unique_user_id=unique_user_id, license_key=license_key)
    if rel_result == False:
        return jsonify({"success":-1, "message": "关联用户失败"}), 200

    # 如果用户存在，则创建 JWT access token
    jwt = generate_unique_user_jwt(unique_user_id=unique_user_id)
    if jwt[0] == "":
        return jsonify({"success":-1, "message": "生成失败"}), 200
    return jsonify({"success":1, "jwt": jwt[0], "expiredAt":jwt[1].strftime("%Y-%m-%d %H:%M:%S")}), 200

@user_controller.route('/user/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
