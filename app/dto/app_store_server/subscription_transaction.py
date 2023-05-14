
from datetime import datetime

class SubscriptionTransaction:

    bundleId: str 
    deviceVerification: str
    deviceVerificationNonce: str 
    environment: str

    # 订阅过期或者续订时间
    expiresDate: datetime 

    # 交易是由用户购买还是通过家庭共享可用的字符串
    inAppOwnershipType: str 

    # 促销优惠类型
        # 1 - 报价
        # An introductory offer.
        # 2 - 促销
        # A promotional offer.
        # 3 - 优惠码
        # An offer with a subscription offer code.
    offerType: int 
    originalPurchaseDate: datetime 
    originalTransactionId: str 
    productId: str 
    purchaseDate: datetime
    quantity: int 
    signedDate: datetime 
    subscriptionGroupIdentifier: str
    transactionId: str 
    type: str

    # 跨设备唯一id
    webOrderLineItemId: str 

    def __init__(self, bundleId=None,deviceVerification=None,deviceVerificationNonce=None,environment=None,expiresDate=None,inAppOwnershipType=None,offerType=None,originalPurchaseDate=None,originalTransactionId=None,productId=None,purchaseDate=None,quantity=None,signedDate=None,subscriptionGroupIdentifier=None,transactionId=None,type=None,webOrderLineItemId=None):
        self.bundleId = bundleId
        self.deviceVerification = deviceVerification
        self.deviceVerificationNonce = deviceVerificationNonce
        self.environment = environment
        self.expiresDate = expiresDate
        self.inAppOwnershipType = inAppOwnershipType
        self.offerType = offerType
        self.originalPurchase_date = originalPurchaseDate
        self.originalTransactionId = originalTransactionId
        self.productId = productId
        self.purchaseDate = purchaseDate
        self.quantity = quantity
        self.signedDate = signedDate
        self.subscriptionGroupIdentifier = subscriptionGroupIdentifier
        self.transactionId = transactionId
        self.type = type
        self.webOrderLineItemId = webOrderLineItemId
    
    # @staticmethod
    # def fromJson(self, json):
    #     return SubscriptionTransaction()
    #     self.bundleId = json["bundleId"]
    #     if "deviceVerification" in json:
    #         self.deviceVerification = json["deviceVerification"]
    #     if "deviceVerification" in json:
    #         self.device_verification_nonce = json["deviceVerificationNonce"]
    #     self.environment = json["environment"]
    #     self.expiresDate = json["expiresDate"]
    #     self.inAppOwnershipType = json["inAppOwnershipType"]
    #     if "offerType" in json:
    #         self.offerType = json["offerType"]
    #     self.originalPurchaseDate = json["originalPurchaseDate"]
    #     self.originalTransactionId = json["originalTransactionId"]
    #     self.productId = json["productId"]
    #     self.purchaseDate = json["purchaseDate"]
    #     self.quantity = json["quantity"]
    #     self.signedDate = json["signedDate"]
    #     self.subscriptionGroupIdentifier = json["subscriptionGroupIdentifier"]
    #     self.transactionId = json["transactionId"]
    #     if "type" in json:
    #         self.type = json["type"]
    #     self.webOrderLineItemId = json["webOrderLineItemId"]

    def __repr__(self):
        return f'<Subscription {self.productId} ({self.type})>'
    

# 续订信息
class SubscriptionRenewalInfo:

    #过期原因
        # 1 - 用户取消
        # The customer canceled their subscription.
        # 2 - 订单错误
        # Billing error; for example, the customer’s payment information is no longer valid.
        # 3 - 用户不同意自动续费，到期取消
        # The customer didn’t consent to an auto-renewable subscription price increase that requires customer consent, allowing the subscription to expire.
        # 4 - 商品不可购买
        # The product wasn’t available for purchase at the time of renewal.
        # 5 - 其他原因
        # The subscription expired for some other reason.
    expirationIntent: int
    originalTransactionId: str
    autoRenewProductId: str
    productId: str
    # 自定续订状态
        # 0 - 关闭
        # Automatic renewal is off. The customer has turned off automatic renewal for the subscription, and it won’t renew at the end of the current subscription period.
        # 1 - 开启
        # Automatic renewal is on. The subscription renews at the end of the current subscription period.
    autoRenewStatus: int
    #应用商店是否正在尝试自动续订过期订
    isInBillingRetryPeriod: bool
    signedDate: datetime
    environment: str
    #自动续订订阅的最早开始日期，忽略间隔小于60天的情况
    recentSubscriptionStartDate: datetime
    
    def __init__(self, expirationIntent=None,originalTransactionId=None,autoRenewProductId=None,productId=None,autoRenewStatus=None,isInBillingRetryPeriod=False,signedDate=None,environment=None,recentSubscriptionStartDate=None):
        self.expirationIntent = expirationIntent
        self.originalTransactionId = originalTransactionId
        self.autoRenewProductId = autoRenewProductId
        self.productId = productId
        self.autoRenewStatus = autoRenewStatus
        self.isInBillingRetryPeriod = isInBillingRetryPeriod
        self.signedDate = signedDate
        self.environment = environment
        self.recentSubscriptionStartDate = recentSubscriptionStartDate


# 订阅交易状态
class SubscriptionStatusGroupTransaction:

    originalTransactionId: str
    # 订阅装填 
        # 1 - 有效
        # The auto-renewable subscription is active.
        # 2 - 过期
        # The auto-renewable subscription is expired.
        # 3 - 订单重试中
        # The auto-renewable subscription is in a billing retry period.
        # 4 - 宽恕期
        # The auto-renewable subscription is in a billing grace period.
        # 5 - 取消
        # The auto-renewable subscription is revoked.
    status: int
        
    # 交易信息
    transactionInfo: SubscriptionTransaction
    # 续订信息
    renewalInfo: SubscriptionRenewalInfo
    
    def __init__(self, originalTransactionId, status, transactionInfo:SubscriptionTransaction, renewalInfo:SubscriptionRenewalInfo):
        self.originalTransactionId = originalTransactionId
        self.status = status
        self.transactionInfo = transactionInfo
        self.renewalInfo = renewalInfo

    def __init__(self, originalTransactionId, status):
        self.originalTransactionId = originalTransactionId
        self.status = status

    def is_active(self):
        return self.status == 1 or self.status == 3 or self.status == 4
    
class SubscriptionStatusGroupInfo:
    # 订阅组id
    subscriptionGroupIdentifier: str

    # 最近的交易列表
    ## The most recent App Store-signed transaction information and App Store-signed renewal information for an auto-renewable subscription.
    lastTransactionList: list[SubscriptionStatusGroupTransaction]

    def __init__(self, subscriptionGroupIdentifier, lastTransactionList:list[SubscriptionStatusGroupTransaction]):
        self.subscriptionGroupIdentifier = subscriptionGroupIdentifier
        self.lastTransactionList = lastTransactionList
    
    def __repr__(self):
        return f'<SubscriptionStatusGroupInfo {self.subscriptionGroupIdentifier} ({len(self.lastTransactionList)})>'

# 订阅状态查询的返回对象
class SubscriptionsStatus:
    # 环境 
    environment:str
    bundleId: str
    #订阅分组列表（一般只有一个数据） - 
    subscriptionGroupList:list[SubscriptionStatusGroupInfo]

    def __init__(self, environment, bundleId:str, subscriptionGroupList:list[SubscriptionStatusGroupInfo]):
        self.environment = environment
        self.bundleId = bundleId
        self.subscriptionGroupList = subscriptionGroupList

    def get_last_transactions(self):
        # print("get_last_transactions")
        if self.subscriptionGroupList and len(self.subscriptionGroupList) > 0 :
            # print("get_last_transactions - has subscriptionGroupList")
            for sub_group in self.subscriptionGroupList:
                if sub_group and hasattr(sub_group, 'lastTransactionList'):
                    # print("get_last_transactions - has lastTransactionList")
                    return sub_group.lastTransactionList
                # else:
                    # print("get_last_transactions - no lastTransactionList")
        
        return 
    
    def __json__(self):
        return {
            'environment': self.environment,
            'bundleId': self.bundleId,
            'subscriptionGroupList':self.subscriptionGroupList
        }