from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required,get_jwt_identity
from repository.license_key_repository import create_license_key, revoke_license_key
from service.apple_uniqe_user_service import regenerate_license_key
from datetime import datetime, timedelta
import uuid
import os

license_key_controller = Blueprint('license_key', __name__)

#重新生成LicenseKey
@license_key_controller.route('/licensekey/regenerate', methods=['POST'])
@jwt_required()
def regenerate():
    unique_user_id = get_jwt_identity()
    licenseKey = request.json.get('licenseKey')
    
    gen_result = regenerate_license_key(unique_user_id=unique_user_id, license_key=licenseKey)
    
    if gen_result[0] == False:
        return jsonify({"successs":-1, "message":gen_result[1]})

    return jsonify({"successs":1, "licenseKey":gen_result[1]})
