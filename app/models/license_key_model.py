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
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def can_use(self):
        return self.state == 1
    
    def is_invalid(self):
        return self.state == 2 or self.state == 3

