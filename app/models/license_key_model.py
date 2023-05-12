from db.db import mysql as db
from datetime import datetime 

class LicenseKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(64), nullable=False)
    state = db.Column(db.Integer, nullable=False, default=0)
    expired_at = db.Column(db.DateTime, nullable=True)
    generated_at = db.Column(db.DateTime, nullable=False)
    revocation_at = db.Column(db.DateTime, nullable=True)
    revocation_reason = db.Column(db.Integer, nullable=True, default=0)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

