# AI订阅管理服务

import os

from service.app_store_server_service import get_subscription_status

AI_SUBSCRIPTION_PRODUCT_ID_PREFIX = os.environ.get("AI_SUBSCRIPTION_PRODUCT_ID_PREFIX")

# 根据根订单获取订阅状态
# SubscriptionsStatus OR NONE
def get_subscription_status_by_ortrid(original_transaction_id):
    if not original_transaction_id:
        return 
    
    return get_subscription_status(original_transaction_id=original_transaction_id)
    
# 根据原始订单查询订阅状态
# response: SubscriptionStatusGroupTransaction - 有效， NONE - 失效
def get_active_subscription_last_transaction(original_transaction_id):
    if not original_transaction_id:
        return 

    subscription_status = get_subscription_status(original_transaction_id=original_transaction_id)
    if not subscription_status:
        return 
    
    last_transactions = subscription_status.get_last_transactions()
    if not last_transactions or len(last_transactions) == 0:
        return
    
    # print(f"check subscription status - last transactions count {len(last_transactions)}")
    active_last_transactions = [t for t in last_transactions if t.is_active() ]
    # print(f"check subscription status - active transactions count {len(active_last_transactions)}")
    if len(active_last_transactions) == 0:
        return 
    else:
        return active_last_transactions[0]
    

    
    
    
