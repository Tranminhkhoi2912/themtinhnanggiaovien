from functools import wraps
from flask import request, jsonify
import jwt # type: ignore
from .teacher.service_teacher import SECRET_KEY # type: ignore
import logging

# Cấu hình logging
logging.basicConfig(filename='teacher.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def teacher_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split(" ")
            if len(parts) == 2:
                token = parts[1]

        if not token:
            logging.error("Truy cập bị từ chối: Token không tồn tại")
            return jsonify({"error": "Token không tồn tại"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if data.get('role') not in ['teacher', 'admin']:
                logging.error(f"Truy cập bị từ chối: Vai trò không hợp lệ (role: {data.get('role')})")
                return jsonify({"error": "Không có quyền truy cập"}), 403
            logging.info(f"Xác thực thành công: teacher_id={data.get('teacher_id')}, role={data.get('role')}")
        except jwt.ExpiredSignatureError:
            logging.error("Truy cập bị từ chối: Token hết hạn")
            return jsonify({"error": "Token hết hạn"}), 401
        except jwt.InvalidTokenError:
            logging.error("Truy cập bị từ chối: Token không hợp lệ")
            return jsonify({"error": "Token không hợp lệ"}), 401

        return f(*args, **kwargs)
    return decorated