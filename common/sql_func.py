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


def call_stored_procedure(user, password, stored_proc_name, *params):
    """
    Kết nối đến MySQL và gọi một Stored Procedure bất kỳ.

    Tham số:
        - user (str): Tên người dùng MySQL.
        - password (str): Mật khẩu MySQL.
        - stored_proc_name (str): Tên stored procedure cần gọi.
        - *params: Các tham số truyền vào stored procedure.

    Ví dụ:
        call_stored_procedure("dev", "12345678x@X", "InsertTestData", "Alice", 22)
        call_stored_procedure("dev", "12345678x@X", "UpdateUserAge", 5, 30)
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
            cursor.callproc(stored_proc_name, params)
            result = cursor.fetchall()

            if result:
                print(f"✅ Stored Procedure '{stored_proc_name}' thực thi thành công! Kết quả: {result}")
            else:
                print(f"⚠ Stored Procedure '{stored_proc_name}' không trả về dữ liệu!")

        conn.commit()
    except pymysql.MySQLError as err:
        print(f"❌ Lỗi khi gọi stored procedure '{stored_proc_name}': {err}")
    finally:
        conn.close()
