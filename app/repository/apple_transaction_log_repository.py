from datetime import datetime
from db.db import mysql
from models.apple_transaction_log_model import AppleTransactionLog

def get_by_transaction_id(transaction_id): 
    if not transaction_id:
        # 单据id为空
        return 
    
    appleTransactionLog = AppleTransactionLog.query.filter_by(transaction_id = transaction_id).first()
    return appleTransactionLog
    

def generate_transaction(transaction_data):
    if not transaction_data:
        return 
    # 增加数据
    transaction = AppleTransactionLog(
        transaction_id = transaction_data["transactionId"],
        original_transaction_id = transaction_data["originalTransactionId"],
        bundle_id = transaction_data["bundleId"],
        environment = transaction_data["environment"],
        in_app_ownership_type = transaction_data["inAppOwnershipType"],
        product_id = transaction_data["productId"],
        
        quantity = transaction_data["quantity"],
        subscription_group_identifier = transaction_data["subscriptionGroupIdentifier"],
        type = transaction_data["type"],
        web_order_line_item_id = transaction_data["webOrderLineItemId"],
    )
    if "expiresDate" in transaction_data:
        transaction.expires_date = datetime.fromtimestamp(transaction_data["expiresDate"] / 1000)
    
    if "originalPurchaseDate" in transaction_data:
        transaction.original_purchase_date = datetime.fromtimestamp(transaction_data["originalPurchaseDate"] / 1000)

    if "purchaseDate" in transaction_data:
        transaction.purchase_date = datetime.fromtimestamp(transaction_data["purchaseDate"] / 1000)

    if "signedDate" in transaction_data:
        transaction.signed_date = datetime.fromtimestamp(transaction_data["signedDate"] / 1000)

    if "isUpgraded" in transaction_data:
        transaction.is_upgraded = transaction_data["isUpgraded"]  
    if "deviceVerification" in transaction_data :
        transaction.device_verification = transaction_data["deviceVerification"]
    if "appAccountToken" in transaction_data :
        transaction.app_account_token = transaction_data["appAccountToken"]
    
    if "revocationDate" in transaction_data :
        transaction.revocation_date = transaction_data["revocationDate"]
    if "revocationReason" in transaction_data :
        transaction.revocation_reason = transaction_data["revocationReason"]
    if "offerType" in transaction_data :
        transaction.offer_type = transaction_data["offerType"]
    if "offerIdentifier" in transaction_data :
        transaction.offer_identifier = transaction_data["offerIdentifier"]
        
    mysql.session.add(transaction)

    # 连接数据库,添加进MySQL中
    mysql.session.commit()


    