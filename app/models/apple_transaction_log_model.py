from db.db import mysql as db
from datetime import datetime 

class AppleTransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(32), nullable=False)
    original_transaction_id = db.Column(db.String(32), nullable=False)
    bundle_id = db.Column(db.String(64), nullable=False)
    environment = db.Column(db.String(64), nullable=False)
    expires_date = db.Column(db.TIMESTAMP(6), nullable=True)
    in_app_ownership_type = db.Column(db.String(16), nullable=True)
    is_upgraded = db.Column(db.SmallInteger, nullable=False, default=0)
    original_purchase_date = db.Column(db.TIMESTAMP(6), nullable=False)
    product_id = db.Column(db.String(64), nullable=False, default='')
    purchase_date = db.Column(db.TIMESTAMP(6), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    signed_date = db.Column(db.TIMESTAMP(6), nullable=True)
    subscription_group_identifier = db.Column(db.String(16), nullable=False, default='')
    type = db.Column(db.String(64), nullable=False, default='')
    web_order_line_item_id = db.Column(db.String(64), nullable=False, default='')
    device_verification = db.Column(db.String(64), nullable=False, default='')
    app_account_token = db.Column(db.String(128), nullable=False, default='')
    revocation_date = db.Column(db.TIMESTAMP(6), nullable=True)
    revocation_reason = db.Column(db.Integer, nullable=True)
    offer_type = db.Column(db.Integer, nullable=True)
    offer_identifier = db.Column(db.String(64), nullable=True, default='')

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

