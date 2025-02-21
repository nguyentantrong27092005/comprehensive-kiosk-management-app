import mysql.connector

def fetch_data(user, password, query, host="34.101.167.101", database="test_db"):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    except mysql.connector.Error as err:
        print(f"Lỗi kết nối: {err}")
        return None

# Truy vấn để lấy dữ liệu từ bảng fooditem
query = "SELECT * FROM fooditem;"
data = fetch_data("dev", "12345678x@X", query)

if data:
    print("Dữ liệu từ bảng fooditem:")
    for row in data:
        print(row)