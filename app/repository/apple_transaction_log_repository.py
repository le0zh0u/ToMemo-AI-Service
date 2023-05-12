from db.db import mysql
from utils.json_util import CustomJSONEncoder
from models.apple_transaction_log_model import AppleTransactionLog

def getByTransactionId(transaction_id): 
    if not transaction_id:
        # 单据id为空
        return 
    
    appleTransactionLog = AppleTransactionLog.query.filter_by(transaction_id = transaction_id).first()
    if not appleTransactionLog:
        return 
    
    return appleTransactionLog
    