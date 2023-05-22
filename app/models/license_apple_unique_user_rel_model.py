from db.db import mysql as db
from datetime import datetime 

class LicenseAppleUniqueUserRel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_key_id = db.Column(db.Integer, nullable=False)
    unique_user_id = db.Column(db.String(64), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)



