import uuid
from datetime import datetime

from dto.app_store_server.subscription_transaction import SubscriptionStatusGroupTransaction, SubscriptionsStatus

from repository.license_key_repository import create_license_key, get_license_key_by_id, active_license_key_with_expired_at, expire_license_key
from repository.license_transaction_rel_repository import add_license_transa_rel, update_license_trans_rel_with_license_key, get_by_original_transaction_id

from models.license_transaction_rel import LicenseTransactionRel

def create_license_key_with_sub_trans(status_group_transaction:SubscriptionStatusGroupTransaction):
    if not status_group_transaction:
        return 
    
    # 将秒级别的时间戳转换为datetime对象
    key = str(uuid.uuid4()).replace('-', '').upper()
    key_id = create_license_key(key, datetime.fromtimestamp(status_group_transaction.transactionInfo.expiresDate / 1000))
    if not key_id:
        return 

    # add rel
    add_rel = add_license_transa_rel(
        key_id, status_group_transaction.transactionInfo.transactionId, status_group_transaction.originalTransactionId, key_id, key
    )

    if add_rel:
        return key
    else :
        return   
    

def active_license_key_with_transaction(active_last_transaction:SubscriptionStatusGroupTransaction, rel:LicenseTransactionRel):
    if not active_last_transaction:
        return 
    
    # 检查license_key是否还有效
    license_key_id = rel.license_key_id
    license_key = get_license_key_by_id(license_key_id)

    if license_key.state == 3:
        # 如果key被重置了，则不处理
        return 
    
    if not license_key :
        # 没有找到关联的LicenseKey，重新创建一个，并更新关联
        key = str(uuid.uuid4()).replace('-', '').upper()

        key_id = create_license_key(key, datetime.fromtimestamp(active_last_transaction.transactionInfo.expiresDate / 1000))
        if not key_id:
            return 
        # 更新关联关系
        update_license_trans_rel_with_license_key(rel.id, key, key_id)
    else :
        # 更新状态和过期时间x
        transa_expires_at = datetime.fromtimestamp(active_last_transaction.transactionInfo.expiresDate / 1000)
        if license_key.expired_at != transa_expires_at and  transa_expires_at > datetime.now():
            # 过期时间不一致, 更新license 过期时间
            active_license_key_with_expired_at(license_key.id, transa_expires_at)
        
def reset_license_key_with_transaction(original_transaction_id):
    if not original_transaction_id or original_transaction_id == "":
        return 
    
    # 根据original_transaction_id获取关联的licenseKey
    license_key_rel = get_by_original_transaction_id(id=original_transaction_id)
    
    if license_key_rel:
        # 存在关系
        key_id = license_key_rel.license_key_id
        if key_id:
            license_key = get_license_key_by_id(id=key_id)
            if license_key and (license_key.state == 0 or license_key.state == 1):
                # license key 有效， 设置为过期
                expire_license_key(id=key_id)
    
    

