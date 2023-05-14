import os, requests, json

from utils.apple_store_kit import get_request_token, encodeSignedData
from dto.app_store_server.subscription_transaction import SubscriptionsStatus,SubscriptionStatusGroupInfo,SubscriptionStatusGroupTransaction, SubscriptionTransaction, SubscriptionRenewalInfo

APP_STORE_CONNECT_STORE_KIT_ENDPOINT = "https://api.storekit-sandbox.itunes.apple.com"

# 连接苹果后台的服务，所有的请求都从这里来

# 自定义序列化函数
def custom_object_encoder(obj):
    if hasattr(obj, '__json__') and callable(obj.__json__):
        return obj.__json__()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def get_subscription_status(original_transaction_id):
    if not original_transaction_id:
        return 
    # 请求链接和参数
    url = APP_STORE_CONNECT_STORE_KIT_ENDPOINT + "/inApps/v1/subscriptions/" + original_transaction_id
    header = {
        "Authorization": f"Bearer {get_request_token()}"
    }
    
    rs = requests.get(url, headers=header)
    if rs.status_code == 200 :
        data = json.loads(rs.text)
        # print(data)
        # 将数据转化成对象结构 SubscriptionsStatus
        ## build subscriptionGroupList
        group_list = []
        if isinstance(data['data'], list):   # 判断'items'是否为数组
            for groupItem in data['data']:
                transaction_list = []
                if isinstance(groupItem['lastTransactions'], list):   # 判断'lastTransactions'是否为数组
                    for lastTransaction in groupItem['lastTransactions']:
                        ori_tran_id = lastTransaction['originalTransactionId']
                        status = lastTransaction['status']
                        sign_tran = lastTransaction['signedTransactionInfo']
                        sign_renew = lastTransaction['signedRenewalInfo']
                        transaction_status = SubscriptionStatusGroupTransaction(originalTransactionId=ori_tran_id, status=status)
                        # 解析signed的对象
                        tran = encodeSignedData(sign_tran)
                        
                        if tran:
                            # tranjson = json.loads()
                            transaction_status.transactionInfo = SubscriptionTransaction(**tran)
                        
                        renew = encodeSignedData(sign_renew)
                        if renew:
                            # renewjson = json.loads()
                            # Renew
                            # print(renew)
                            transaction_status.renewalInfo = SubscriptionRenewalInfo(**renew)

                        transaction_list.append(transaction_status)
                # print(f"transaction_list count - {len(transaction_list)}")
                group_info = SubscriptionStatusGroupInfo(subscriptionGroupIdentifier=groupItem['subscriptionGroupIdentifier'], lastTransactionList=transaction_list)
                group_list.append(group_info)
        result = SubscriptionsStatus(
            environment = data['environment'],
            bundleId = data['bundleId'],
            subscriptionGroupList= group_list
        )
        return result
    else :
        print("请求失败")
        return 

    
def main():
    print(get_subscription_status("2000000329169549"))

if __name__ == '__main__':
    main()