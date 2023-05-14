import json
from flask import Blueprint, request, jsonify

from repository.apple_transaction_log_repository import get_by_transaction_id, generate_transaction
from repository.license_transaction_rel_repository import get_by_original_transaction_id

from service.ai_subscription_service import get_active_subscription_last_transaction
from service.license_key_service import create_license_key_with_sub_trans, active_license_key_with_transaction, reset_license_key_with_transaction

from dto.app_store_server.subscription_transaction import SubscriptionTransaction

trans_controller = Blueprint('apple_transaction', __name__)
    
@trans_controller.route('/sync/apple/transaction', methods=['POST'])
def syncTransaction():
    original_transaction_id = request.json.get('originalTransactionId')
    transaction_id = request.json.get('transactionId')
    
    if not original_transaction_id or not transaction_id:
        return jsonify({"successs":-1, "message":"苹果单据为空"}), 200, {'Content-Type': 'application/json;charset=utf-8'}
    
    # 将 JSON 数据解析为 Python 字典
    trans = request.json 
    # 将 Python 字典映射为 Subscription 对象
    subscription = SubscriptionTransaction(**trans) # SubscriptionTransaction(**trans)

    # 从苹果查询状态 SubscriptionStatusGroupTransaction or None
    subscription_status = None
    try:    
        subscription_status = get_active_subscription_last_transaction(original_transaction_id)
    except Exception as error:
        print(f"出现异常 - {error}")
        return jsonify({"successs":-1, "message":"苹果单据同步失败"}), 200, {'Content-Type': 'application/json;charset=utf-8'}
    
   # 校验订单是否存在
    app_transaction = get_by_transaction_id(subscription.transactionId)
    if not app_transaction:
        # 订单不存在，新建订单
        generate_transaction(trans)
    
    if subscription_status:
        # 判断订单是否关联LicenseKey
        rel = get_by_original_transaction_id(id=original_transaction_id)
        if not rel: 
            # create license and rel
            key = create_license_key_with_sub_trans(subscription_status)
            if not key:
                return jsonify({"successs":-1, "message":"license key create failed"}), 200, {'Content-Type': 'application/json;charset=utf-8'}    
            else :
                return jsonify({"successs":1, "status": 1, "license_key":key}), 200, {'Content-Type': 'application/json;charset=utf-8'}
        else :
            # 因为订单和licenseKey关联已存在，意味着已经激活过了，需要手动输入LicenseKey
            # 判断licenseKey状态，如果licenseKey过期，需要重置状态
            active_license_key_with_transaction(active_last_transaction=subscription_status, rel=rel)
            return jsonify({"successs":1, "status": 1, "license_key":""}), 200, {'Content-Type': 'application/json;charset=utf-8'}
        
    else:
        # 重置licenseKey
        reset_license_key_with_transaction(original_transaction_id)
        return jsonify({"successs":1, "status": 0}), 200
