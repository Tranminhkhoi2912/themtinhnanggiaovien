import mysql.connector
from app import DB_CONFIG
import logging

# Cấu hình logging
logging.basicConfig(filename='teacher.log', level=logging.INFO, 
      format='%(asctime)s - %(levelname)s - %(message)s')

def get_teacher_by_id(teacher_id):
    """Lấy thông tin giáo viên từ database dựa trên teacher_id."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Teachers WHERE teacher_id = %s AND is_active = 1", (teacher_id,))
        teacher = cursor.fetchone()
        conn.close()
        if teacher:
            logging.info(f"Lấy thông tin giáo viên thành công: teacher_id={teacher_id}")
        else:
            logging.warning(f"Không tìm thấy giáo viên: teacher_id={teacher_id}")
        return teacher
    except mysql.connector.Error as err:
        logging.error(f"Lỗi database khi lấy thông tin giáo viên {teacher_id}: {err}")
        return None

def create_teacher(teacher_id, name, email, password, role='teacher'):
    """Tạo giáo viên mới với mật khẩu đã hash."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        from .service import hash_password  # type: ignore # Import tại đây để tránh circular import
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO Teachers (teacher_id, name, email, password_hash, role, require_password_change, is_active)
            VALUES (%s, %s, %s, %s, %s, 0, 1)
        """, (teacher_id, name, email, password_hash, role))
        conn.commit()
        conn.close()
        logging.info(f"Tạo giáo viên thành công: teacher_id={teacher_id}")
    except mysql.connector.Error as err:
        logging.error(f"Lỗi database khi tạo giáo viên {teacher_id}: {err}")
        conn.close()
        raise