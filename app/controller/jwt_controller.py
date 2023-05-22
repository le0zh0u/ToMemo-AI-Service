from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required,get_jwt_identity, create_refresh_token, decode_token

from service.apple_uniqe_user_service import relate_unique_user_with_license_key, verify_unique_user_id_with_license_key,generate_unique_user_jwt, veriry_for_refresh_token, verify_jwt_token

from datetime import timedelta

jwt_controller = Blueprint('jwt', __name__)

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

@jwt_controller.route('/token/generate', methods=['POST'])
def use_license_key():
    unique_user_id = request.json.get('uniqueUserId')
    license_key = request.json.get('licenseKey')

    if not unique_user_id:
        return jsonify({"success":-1, "message":"用户唯一id为空"}), 200
    
    # 进行身份验证逻辑并检查用户是否存在
    # - LicekseKey是否有效
    # - 关联关系不能多余6条（限制6台设备关联）
    verify_result = verify_unique_user_id_with_license_key(unique_user_id, license_key)
    if verify_result[0] == False:
        return jsonify({"success":-1, "message": verify_result[1]}), 200
        
    
    # 用户关系处理，
    # 如果关联不存在，需要创建userid和license_key的关联关系 
    rel_result = relate_unique_user_with_license_key(unique_user_id=unique_user_id, license_key=license_key)
    if rel_result == False:
        return jsonify({"success":-1, "message": "关联用户失败"}), 200
    
    # 如果用户存在，则创建 JWT access token
    jwt = generate_unique_user_jwt(unique_user_id=unique_user_id)

    if jwt[0] == "":
        return jsonify({"success":-1, "message": "生成失败"}), 200
    
    # refresh_token = create_refresh_token(identity=unique_user_id, expires_delta=timedelta(seconds=20))
    refresh_token = create_refresh_token(identity=unique_user_id)
    result = {"success":1, 
                    "accessToken": jwt[0], 
                    "expiredAt":jwt[1].strftime("%Y-%m-%d %H:%M:%S"),
                    "refreshToken":refresh_token
                    }
    # print(result)
    return jsonify(result), 200

@jwt_controller.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()

    # 根据当前用户校验
    if veriry_for_refresh_token(unique_user_id=current_user) == False:
        # return jsonify({"success":-1, "message": "校验失败"}), 200
        abort(401)

    # 生成新的访问令牌
    jwt_token = generate_unique_user_jwt(unique_user_id=current_user)
    if jwt_token[0] == "":
        return jsonify({"success":-1, "message": "生成失败"}), 200

    # 返回响应
    return jsonify({"success":1, 
                    "accessToken": jwt_token[0], 
                    "expiredAt":jwt_token[1].strftime("%Y-%m-%d %H:%M:%S")
                    }), 200
    

@jwt_controller.route('/token/test', methods=['GET'])
@jwt_required()
def test_token():
    
    current_user = get_jwt_identity()
    auth_header = request.headers.get("Authorization")
    jwt_token = auth_header.split(" ")[1]  # Assuming JWT is in the format "Bearer <JWT>"
    result = verify_jwt_token(unique_user_id=current_user, jwt = jwt_token)
    if result == False:
        abort(401)

    # logged_in_as=current_user
    return jsonify({"success":1})
    
    
    
