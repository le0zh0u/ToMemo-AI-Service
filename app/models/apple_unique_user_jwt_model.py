from db.db import mysql as db
from datetime import datetime 

class AppleUniqueUserJWT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    unique_user_id = db.Column(db.String(64), nullable=False)
    jwt_md5 = db.Column(db.String(32), nullable=False)
    jwt_expired_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)


