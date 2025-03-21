import hashlib
import sys
import pymysql
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QApplication, QStackedWidget
from admin_app.views.LoginAppView import LoginAppWidget
from kiosk_app.models.SharedDataModel import SharedDataModel

class Database_LoginApp:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host="34.101.167.101",
                user="dev",
                password="12345678x@X",
                database="kioskapp",
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
        except pymysql.MySQLError as e:
            print(f"Lỗi kết nối DB: {e}")
            self.connection = None

    def fetch_user(self, email):
        """Lấy thông tin người dùng từ database theo email"""
        if not self.connection:
            print("Không có kết nối đến cơ sở dữ liệu.")
            return None

        query = """SELECT Email, PasswordHash, PasswordSalt FROM user WHERE Email = %s;"""
        try:
            self.cursor.execute(query, (email,))
            return self.cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"Lỗi truy vấn fetch_user: {e}")
            return None

class LoginAppViewEx(LoginAppWidget):
    def __init__(self, mainStackedWidget: QtWidgets.QStackedWidget, sharedData, db):
        super().__init__()
        self.sharedData = sharedData
        self.db = db
        self.mainStackedWidget = mainStackedWidget
        self.setup_connections()

    def setup_connections(self):
        self.LoginButton.clicked.connect(self.handle_login)

    def convert_hash_password(self, password: str, salt: str) -> str:
        salted_password = password + salt
        return hashlib.sha256(salted_password.encode()).hexdigest()

    def handle_login(self):
        email = self.InputEmail.text()
        password = self.InputPassword.text()

        # Kiểm tra xem nhập đủ email và password chưa
        if not email or not password:
            self.errorLabel.setText("Vui lòng nhập đầy đủ email và mật khẩu.")
            self.errorLabel.setVisible(True)
            return

        user_data = self.db.fetch_user(email)
        if user_data:
            stored_hash, salt = user_data["PasswordHash"], user_data["PasswordSalt"]
            hashed_password = self.convert_hash_password(password, salt)

            if hashed_password == stored_hash:
                QMessageBox.information(self, "Thông báo", "Đăng nhập thành công")
            else:
                self.errorLabel.setText("Bạn đã nhập sai mật khẩu.")
                self.errorLabel.setVisible(True)
        else:
            self.errorLabel.setText("Sai email hoặc mật khẩu.")
            self.errorLabel.setVisible(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainStackedWidget = QtWidgets.QStackedWidget()
    sharedData = SharedDataModel()
    db = Database_LoginApp()
    window = LoginAppViewEx(mainStackedWidget, sharedData, db)
    window.show()
    sys.exit(app.exec())
