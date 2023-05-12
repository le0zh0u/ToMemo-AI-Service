from flask import Blueprint, request, jsonify
from models.apple_transaction_log_model import AppleTransactionLog
from repository.apple_transaction_log_repository import getByTransactionId

trans_controller = Blueprint('apple_transaction', __name__)

@trans_controller.route('/apple/transaction/log/check', method=['POST'])
def checkTransaction():
    transactionId = request.json.get('transactionId')
    originalTransactionId = request.json.get('originalTransactionId')

    if not transactionId:
        return jsonify({"successs":-1, "message":"苹果单据为空"}), 200
    if not originalTransactionId:
        return jsonify({"successs":-1, "message":"苹果单据为空"}), 200
    
    # TODO 从苹果查询订单数据

   # 校验订单是否存在
    appleTransaction = getByTransactionId()
    if not appleTransaction:
        #TODO 订单不存在，新建订单
        


    # TODO 判断订单是否关联LicenseKey
    
    
    # TODO 创建用户测试
    # 如果用户存在，则创建 JWT access token
    # access_token = create_access_token(identity=uniqueUserId)
    #TODO 保存jwt到数据库中 userid - jwt
    # return jsonify(access_token=access_token), 200
    return


@user_controller.route('/handle/user', methods=['POST'])
def login():
    uniqueUserId = request.json.get('uniqueUserId')

    if not uniqueUserId:
        return jsonify({"successs":-1, "message":"用户唯一id为空"}), 200
    
    iCloudRecordUserId = request.json.get('iCloudRecordUserId')
    receipts = request.json.get('receipts')

    # 进行身份验证逻辑并检查用户是否存在
    if not verify_user(uniqueUserId, iCloudRecordUserId, receipts):
        return jsonify({"msg": "Bad username or password"}), 401

    # 如果用户存在，则创建 JWT access token
    access_token = create_access_token(identity=uniqueUserId)
    #TODO 保存jwt到数据库中 userid - jwt
    return jsonify(access_token=access_token), 200

def verify_user(usename, password, receipts):

    

    #TODO 用户关系处理，
    # 如果用户不存在，需要新建用户，并创建userid和icloudRecordUserId的关联关系
    # 如果uniqueUserId存在，但是icloudRecordUserId，那么添加关联关系 - 关联关系不能多余6条（限制6台设备关联）
    # 如果uniqueUserId,iCloudRecordUserId存在，根据receipts与苹果服务器校验，如果校验通过，则表示用户已经订阅，如果校验未通过，表示用户未订阅

    #TODO 检验用户是否在黑名单中

    #TODO 检验用户是否已经有jwt，如果已经有了，返回错误

    return True

@user_controller.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
