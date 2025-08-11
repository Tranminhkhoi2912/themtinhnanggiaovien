# file: app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    """
    Hàm "nhà máy" (factory function) để tạo và cấu hình ứng dụng Flask.
    """
    app = Flask(__name__)
    CORS(app)

    # Import và đăng ký Blueprint API cũ
    from .routes import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # Import và đăng ký Blueprint teacher
    from teacher.routes import teacher_bp # type: ignore
    app.register_blueprint(teacher_bp)

    return app
