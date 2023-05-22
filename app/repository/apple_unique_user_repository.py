from datetime import datetime
import hashlib
from db.db import mysql
from models.license_apple_unique_user_rel_model import LicenseAppleUniqueUserRel
from models.apple_unique_user_jwt_model import AppleUniqueUserJWT

def get_license_unique_user_rel_by_unique_user_id(unique_user_id:str): 
    if unique_user_id == "":
        return 
    
    rel = LicenseAppleUniqueUserRel.query.filter_by(unique_user_id = unique_user_id).first()
    return rel

def fetch_license_unique_user_rel_by_license_id(license_id: int):
    return LicenseAppleUniqueUserRel.query.filter_by(license_key_id = license_id)

def create_license_unique_user_rel(unique_user_id: str, license_key_id: int):
    if unique_user_id == "":
        return 
    rel = LicenseAppleUniqueUserRel(
        unique_user_id = unique_user_id,
        license_key_id = license_key_id
    )

    mysql.session.add(rel)

    # 连接数据库,添加进MySQL中
    mysql.session.commit()

def update_licnese_unique_user_rel(id: int, license_key_id: int):
    rel = LicenseAppleUniqueUserRel.query.filter_by(id = id).first()
    if not rel:
        return 
    rel.license_key_id = license_key_id
    rel.updated_at = datetime.now()

    mysql.session.commit()


def get_unique_user_jwt_by_unique_user_id(unique_user_id:str):
    if unique_user_id == "":
        return 
    
    return AppleUniqueUserJWT.query.filter_by(unique_user_id=unique_user_id).first()

def rel_unique_user_jwt(unique_user_id: str, jwt: str, expired_at: datetime):
    if unique_user_id == "" or jwt == "":
        return False
    
    md5 = hashlib.md5()

    # 更新 MD5 对象的内容
    md5.update(jwt.encode('utf-8'))

    # 获取加密后的结果
    jwt_md5 = md5.hexdigest()

    # 是否存在
    existed_rel = get_unique_user_jwt_by_unique_user_id(unique_user_id=unique_user_id)
    if existed_rel:
        existed_rel.jwt_md5 = jwt_md5
        existed_rel.updated_at = datetime.now()
    else:
        rel = AppleUniqueUserJWT(
            unique_user_id = unique_user_id,
            jwt_md5 = jwt_md5,
            jwt_expired_at = expired_at
        )

        mysql.session.add(rel)

    # 连接数据库,添加进MySQL中
    mysql.session.commit()

    return True

