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

