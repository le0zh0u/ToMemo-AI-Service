from db.db import mysql
from models.license_key_model import LicenseKey
from datetime import datetime


def create_license_key(key:str, expired_at:datetime):
    if not key or not expired_at:
        return 
    
    # 增加数据
    license_key = LicenseKey(
        license_key = key,
        expired_at = expired_at,
        generated_at = datetime.now()
    )

    mysql.session.add(license_key)
    # 连接数据库,添加进MySQL中
    mysql.session.commit()

    return license_key.id

def get_license_key_by_id(id:int): 
    return LicenseKey.query.filter_by(id = id).first()

def expire_license_key(id:int):
    key = LicenseKey.query.filter_by(id = id).first()

    key.expired_at = datetime.now()
    key.state = 2
    key.updated_at = datetime.now()

    mysql.session.commit()

def active_license_key_with_expired_at(id: int, expired_at: datetime):
    key = LicenseKey.query.filter_by(id = id).first()

    key.expired_at = expired_at
    key.state = 1
    key.updated_at = datetime.now()

    mysql.session.commit()