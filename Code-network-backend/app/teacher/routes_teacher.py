from flask import Blueprint, request, jsonify
import logging
from .model import get_teacher_by_id # type: ignore
from .service import check_password, generate_token # type: ignore

# Cấu hình logging
logging.basicConfig(filename='teacher.log', level=logging.INFO, 
   format='%(asctime)s - %(levelname)s - %(message)s')

teacher_bp = Blueprint('teacher_bp', __name__)

@teacher_bp.route('/api/teacher/login', methods=['POST'])
def teacher_login():
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    password = data.get('password')

    # Kiểm tra dữ liệu đầu vào
    if not teacher_id or not password or not teacher_id.strip() or not password.strip():
        logging.error(f"Đăng nhập thất bại: ID hoặc mật khẩu trống (teacher_id: {teacher_id})")
        return jsonify({"error": "Vui lòng nhập đầy đủ ID và mật khẩu"}), 400
    if len(teacher_id) > 50 or len(password) > 100:
        logging.error(f"Đăng nhập thất bại: ID hoặc mật khẩu quá dài (teacher_id: {teacher_id})")
        return jsonify({"error": "ID hoặc mật khẩu quá dài"}), 400

    # Lấy thông tin giáo viên
    teacher = get_teacher_by_id(teacher_id)
    if not teacher or not teacher['is_active']:
        logging.error(f"Đăng nhập thất bại: Sai ID hoặc tài khoản bị vô hiệu hóa (teacher_id: {teacher_id})")
        return jsonify({"error": "Sai ID hoặc tài khoản bị vô hiệu hóa"}), 401

    # Kiểm tra mật khẩu
    if not check_password(password, teacher['password_hash']):
        logging.error(f"Đăng nhập thất bại: Sai mật khẩu (teacher_id: {teacher_id})")
        return jsonify({"error": "Sai ID hoặc mật khẩu"}), 401

    # Tạo JWT token
    token = generate_token(teacher['teacher_id'], teacher['role'])
    logging.info(f"Đăng nhập thành công: teacher_id={teacher_id}, role={teacher['role']}")
    return jsonify({
        "message": "Đăng nhập thành công",
        "teacher_id": teacher['teacher_id'],
        "role": teacher['role'],
        "token": token
    })