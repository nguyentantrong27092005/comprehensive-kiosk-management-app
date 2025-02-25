import pymysql

def fetch_data(user, password, query, host="34.101.167.101", database="test_db"):
    """
    Truy vấn dữ liệu từ cơ sở dữ liệu.
    Ví dụ sử dụng:
    --------------
    query = "SELECT * FROM fooditem;"
    data = fetch_data("dev", "12345678x@X", query)
    Nếu có dữ liệu, sẽ hiển thị như sau:
    -------------------------------------
    Dữ liệu từ bảng fooditem:
    (row1_data)
    (row2_data)
    ...
    Tham số:
    --------
    user : str
        Tên đăng nhập vào cơ sở dữ liệu.
    password : str
        Mật khẩu đăng nhập.
    query : str
        Câu lệnh SQL cần thực thi.
    Trả về:
    -------
    list
        Danh sách các dòng dữ liệu từ truy vấn.
    """
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.Cursor  # Dùng Cursor để lấy dữ liệu dạng tuple
        )
        cursor = conn.cursor()

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    except pymysql.MySQLError as err:
        print(f"Lỗi kết nối: {err}")
        return None
import pymysql

def insert_user_data(user, password, name, age):
    """Kết nối đến MySQL và gọi Stored Procedure InsertTestData"""
    """
    # Gọi hàm để chèn dữ liệu
    insert_user_data("dev", "12345678x@X", "Alice", 22)
    insert_user_data("dev", "12345678x@X", "Bob", 25)
    """
    try:
        conn = pymysql.connect(
            host="34.101.167.101",
            user=user,
            password=password,
            database="test_db",
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            cursor.callproc("InsertTestData", (name, age))
            result = cursor.fetchall()  # Lấy kết quả trả về

            if result and "NewID" in result[0]:
                print(f"✅ Dữ liệu đã chèn thành công! ID: {result[0]['NewID']}")
            else:
                print("⚠ Không có dữ liệu trả về!")

        conn.commit()
    except pymysql.MySQLError as err:
        print(f"❌ Lỗi khi chèn dữ liệu: {err}")
    finally:
        conn.close()


