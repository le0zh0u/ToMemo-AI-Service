from flask import Blueprint, request, jsonify, abort
from repository.license_key_repository import create_license_key, revoke_license_key
from datetime import datetime, timedelta
import uuid
import os

license_key_admin_controller = Blueprint('license_key_admin', __name__)

@license_key_admin_controller.route('/admin/licensekey/generate', methods=['POST'])
def generate_license_key():
    
    admin_key = request.headers.get("admin-key")
    if not admin_key or admin_key == "":
        abort(401)
    print(f"admin_key - {admin_key}")
    valid_key = os.environ.get("ADMIN_KEY")
    print(f"valid_key - {valid_key}")
    if valid_key != admin_key:
        abort(401)

    key = str(uuid.uuid4()).replace('-', '').upper()
    one_year_later = datetime.now() + timedelta(days=3650)
    create_license_key(key=key, expired_at= one_year_later)
    
    return jsonify({"successs":1, "key":key})


@license_key_admin_controller.route('/admin/licensekey/revoke', methods=['POST'])
def revoke_license_key():

    admin_key = request.headers.get("admin-key")
    if not admin_key or admin_key == "":
        abort(401)
    
    valid_key = os.environ.get("ADMIN_KEY")
    if valid_key != admin_key:
        abort(401)

    data = request.get_json()
    license_key = data["key"]
    
    revoke_license_key(license_key)

    return jsonify({"successs":1})
