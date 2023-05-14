from db.db import mysql
from models.license_transaction_rel import LicenseTransactionRel


def get_by_original_transaction_id(id:str): 
    if not id or id == "":
        # 单据id为空
        return 
    
    license_transaction_rel = LicenseTransactionRel.query.filter_by(original_transaction_id = id).first()
    return license_transaction_rel
    

def add_license_transa_rel(apple_transaction_log_id:int, 
        transaction_id: str, 
        original_transaction_id:str,
        license_key_id:int,
        license_key:str):
    
    if transaction_id == "" or original_transaction_id == "":
        return False
    
    rel = LicenseTransactionRel(
        apple_transaction_log_id = apple_transaction_log_id,
        transaction_id = transaction_id,
        original_transaction_id = original_transaction_id,
        license_key_id = license_key_id,
        license_key = license_key
    )

    mysql.session.add(rel)
    # 连接数据库,添加进MySQL中
    mysql.session.commit()

    return True

def update_license_trans_rel_with_license_key(id: int, key:str, key_id: int):
    
    rel = LicenseTransactionRel.query.filter_by(id = id).first()
    if not rel:
        return 
    
    rel.license_key_id = key_id
    rel.license_key = key

    mysql.session.commit()