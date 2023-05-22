from db.db import mysql as db
from datetime import datetime 

class LicenseKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(64), nullable=False)
    # 状态 0 - 未激活， 1 - 已激活, 2 - 已过期, 3 - 已作废
    state = db.Column(db.Integer, nullable=False, default=0)
    expired_at = db.Column(db.DateTime, nullable=True)
    generated_at = db.Column(db.DateTime, nullable=False)
    revocation_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def is_unactive(self):
        return self.state == 0

    def can_use(self):
        return self.state == 1
    
    def is_revoke(self):
        return self.state == 3
    
    def is_expired(self):
        return self.state == 2
    
    def is_invalid(self):
        return self.is_expired() or self.is_revoke()

