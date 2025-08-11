import os
import hashlib
import jwt # type: ignore
import datetime
import logging

# Cấu hình logging
logging.basicConfig(filename='teacher.log', level=logging.INFO, 
   format='%(asctime)s - %(levelname)s - %(message)s')

# Lấy SECRET_KEY từ biến môi trường, mặc định cho test
SECRET_KEY = os.environ.get('SECRET_KEY', 'day_la_secret_key_cua_ban')

def hash_password(password):
    """Mã hóa mật khẩu với salt ngẫu nhiên."""
    try:
        salt = os.urandom(16).hex()  # Tạo salt ngẫu nhiên
        salted_password = password + salt
        password_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        logging.info(f"Tạo hash mật khẩu thành công cho password (dài {len(password)} ký tự)")
        return f"{salt}:{password_hash}"
    except Exception as e:
        logging.error(f"Lỗi khi tạo hash mật khẩu: {e}")
        raise

def check_password(password, stored_hash):
    """Kiểm tra mật khẩu bằng cách so sánh hash."""
    try:
        # Tách salt và hash từ giá trị lưu trữ
        salt, password_hash = stored_hash.split(":")
        # Tạo lại hash từ password và salt
        salted_password = password + salt
        computed_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        return computed_hash == password_hash
    except ValueError:
        # Hỗ trợ hash cũ không có salt (cho tương thích với dữ liệu cũ)
        logging.warning("Kiểm tra mật khẩu bằng hash không có salt (hệ thống cũ)")
        return hashlib.sha256(password.encode()).hexdigest() == stored_hash
    except Exception as e:
        logging.error(f"Lỗi khi kiểm tra mật khẩu: {e}")
        return False

def generate_token(teacher_id, role):
    """Tạo JWT token với thời hạn 4 giờ."""
    try:
        token = jwt.encode(
            {
                "teacher_id": teacher_id,
                "role": role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=4)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        logging.info(f"Tạo token thành công cho teacher_id={teacher_id}")
        return token
    except Exception as e:
        logging.error(f"Lỗi khi tạo JWT token: {e}")
        raise