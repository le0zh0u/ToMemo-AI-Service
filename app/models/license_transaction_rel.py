from db.db import mysql as db
from datetime import datetime 

class LicenseTransactionRel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apple_transaction_log_id = db.Column(db.Integer, nullable=False)
    transaction_id = db.Column(db.String(32), nullable=False)
    original_transaction_id = db.Column(db.String(32), nullable=False)
    license_key_id = db.Column(db.Integer, nullable=False)
    license_key = db.Column(db.String(64), nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
