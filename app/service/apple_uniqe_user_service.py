import os, hashlib
from datetime import datetime, timedelta
from repository.apple_unique_user_repository import get_license_unique_user_rel_by_unique_user_id, create_license_unique_user_rel, fetch_license_unique_user_rel_by_license_id, rel_unique_user_jwt, update_licnese_unique_user_rel, get_unique_user_jwt_by_unique_user_id
from repository.license_key_repository import get_license_key_by_key, active_license_key, get_license_key_by_id, revoke_license_key,expire_license_key
from service.license_key_service import regenerate_license_key_by_unique_user_id

from flask_jwt_extended import create_access_token

# 关联苹果独立用户和LicenseKey的关系
# 如果用户不存在，需要创建userid和license_key的关联关系 - 关联关系不能多余6条（限制6台设备关联）
# 如果uniqueUserId,license_key存在，根据receipts与苹果服务器校验，如果校验通过，则表示用户已经订阅，如果校验未通过，表示用户未订阅
def relate_unique_user_with_license_key(unique_user_id:str, license_key:str) :
    if unique_user_id == "" or license_key == "":
        return False
    
    # get license key
    license = get_license_key_by_key(key=license_key)
    if not license:
        return False
    
    # get by unique_user_id
    user_license_rel = get_license_unique_user_rel_by_unique_user_id(unique_user_id=unique_user_id)
    if not user_license_rel:
        create_license_unique_user_rel(unique_user_id=unique_user_id, license_key_id=license.id)
    else:
        # 存在License关系，更新 
        if user_license_rel.license_key_id != license.id:
            update_licnese_unique_user_rel(id=user_license_rel.id, license_key_id=license.id)

    return True

def veriry_for_refresh_token(unique_user_id:str):
    if unique_user_id == "":
        return False
    user_license_rel = get_license_unique_user_rel_by_unique_user_id(unique_user_id=unique_user_id)
    if not user_license_rel:
        return False
    
    license_key_id = user_license_rel.license_key_id
    if  license_key_id == "":
        return False
    
    license = get_license_key_by_id(license_key_id)
    if not license:
        return False
    
    return license.can_use()


def generate_unique_user_jwt(unique_user_id: str):
    if unique_user_id == "":
        return "", None    
    
    jwt_expired_at = datetime.now() + timedelta(days=1)
    access_token = create_access_token(unique_user_id, fresh = False, expires_delta=timedelta(days=1))
    # jwt_expired_at = datetime.now() + timedelta(seconds=10)
    # access_token = create_access_token(unique_user_id, fresh = False, expires_delta=timedelta(seconds=10))

    result = rel_unique_user_jwt(unique_user_id=unique_user_id, jwt=access_token,expired_at=jwt_expired_at)
    if result:
        return access_token, jwt_expired_at
    return "", None


def verify_unique_user_id_with_license_key(uniqe_user_id, license_key):

    # 检验用户是否在黑名单中
    user_black_list = os.environ.get("USER_BLACK_LIST")
    if user_black_list and len(user_black_list):
        if uniqe_user_id in user_black_list:
            return False, "用户异常"
        
    #TODO 检验用户是否已经有jwt，如果已经有了，返回错误 - 同一个设备只能有一个jwt
    # user_jwt = get_unique_user_jwt_by_unique_user_id(unique_user_id=uniqe_user_id)
    # if user_jwt:
    #     if user_jwt.jwt == 
    # 需要放在用户带着jwt请求时，进行校验

    # licenseKey 是否有效
    license = get_license_key_by_key(license_key)
    if not license:
        return False, "LicenseKey不存在"
    # 状态 0 - 未激活， 1 - 已激活, 
    if license.is_revoke():
        # 3 - 已作废
        return False, "LicenseKey已失效"
    
    if license.expired_at < datetime.now():
        # 2 - 已过期
        if license.is_unactive() or license.can_use():
            expire_license_key(license.id)
            return False, "LicenseKey已失效"
        elif license.is_expired():
            return False, "LicenseKey已失效"
    
    if license.is_expired() or license.is_unactive():
        # 过期或者未激活，则需要激活
        # active license
        active_license_key(license.id)

    # licenseKey 是否关联过多
    rel_list = fetch_license_unique_user_rel_by_license_id(license_id=license.id)
    
    if rel_list and rel_list.count() >= 5:
        return False, "LicenseKey关联过多"
    
    return True, ""

def regenerate_license_key(unique_user_id:str, license_key: str):
    if unique_user_id == "" or license_key == "":
        return False, "参数为空"
    
    rel = get_license_unique_user_rel_by_unique_user_id(unique_user_id=unique_user_id)
    if not rel:
        return False, "未找到LicenseKey"
    
    license_from_rel = get_license_key_by_id(rel.license_key_id)
    if not license_from_rel:
        return False, "未找到LicenseKey"

    if license_from_rel.license_key != license_key:
        return False, "LicenseKey未匹配"
    
    # license_key一致，执行撤销
    revoke_license_key(license_key)

    # 重新生成
    key = regenerate_license_key_by_unique_user_id(unique_user_id=unique_user_id)
    return True, key
    
    
def verify_jwt_token(unique_user_id:str, jwt:str):
    if unique_user_id == "" or jwt == "":
        return False
    
    license_user_rel = get_license_unique_user_rel_by_unique_user_id(unique_user_id=unique_user_id)
    if not license_user_rel:
        return False
    
    license = get_license_key_by_id(id=license_user_rel.license_key_id)
    if not license :
        return False
    
    if license.can_use() == False or license.expired_at < datetime.now():
        return False
    
    user_jwt_rel = get_unique_user_jwt_by_unique_user_id(unique_user_id=unique_user_id)
    if not user_jwt_rel:
        return False
    
    md5 = hashlib.md5()
    # 更新 MD5 对象的内容
    md5.update(jwt.encode('utf-8'))
    # 获取加密后的结果
    jwt_md5 = md5.hexdigest()
    if user_jwt_rel.jwt_md5 == jwt_md5:
        return True
    
    return False
    
    
