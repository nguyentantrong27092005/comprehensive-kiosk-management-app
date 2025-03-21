import pymysql
import os

from PyQt6.QtWidgets import QMessageBox
from dotenv import load_dotenv
from kiosk_app.models.Order import Order
from datetime import datetime, timedelta



class Database:
    def __init__(self):
        load_dotenv(dotenv_path='.env')
        self.user = os.getenv('USER_DB')
        self.password = os.getenv('PASSWORD_DB')
        self.host = os.getenv('HOST_DB')
        self.port = int(os.getenv('PORT_DB'))
        self.database = os.getenv('DB')
        self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor  # Dùng Cursor để lấy dữ liệu dạng tuple
            )
        self.cursor = self.conn.cursor()

    def fetch_data(self, query, *arg):
        """
        Truy vấn dữ liệu từ cơ sở dữ liệu.
        Ví dụ sử dụng:
        --------------
        query = "SELECT * FROM fooditem WHERE CategoryID = %s;"
        data = fetch_data(query, 1) #Truy vấn danh sách fooditem có nhóm món id là 1
        Nếu có dữ liệu, sẽ hiển thị như sau:
        -------------------------------------
        Dữ liệu từ bảng fooditem:
        (row1_data)
        (row2_data)
        ...
        Tham số:
        --------
        query : str
            Câu lệnh SQL cần thực thi.
        arg: any, any,...
            Các format string cần truyền vào câu query
        Trả về:
        -------
        list
            Danh sách các dòng dữ liệu từ truy vấn.
        """
        try:
            self.cursor.execute(query, arg)
            result = self.cursor.fetchall()

            # cursor.close()
            # conn.close()
            #
            return result

        except pymysql.MySQLError as err:
            print(f"Lỗi kết nối: {err}")
            return None

    def do_any_sql(self, query, *arg):
        """
        Làm hành động bất kì với db (UPDATE, DELETE, INSERT, CREATE,...)
        Ví dụ sử dụng:
        --------------
        query = "UPDATE order SET status = 4 WHERE ID = %s;" #cập nhật trạng thái đơn hàng thành "Đã huỷ"
        data = do_any_sql(query, 1) #Truy vấn danh sách fooditem có nhóm món id là 1
        Nếu có dữ liệu, sẽ hiển thị như sau:
        -------------------------------------
        Dữ liệu từ bảng fooditem:
        (row1_data)
        (row2_data)
        ...
        Tham số:
        --------
        query : str
            Câu lệnh SQL cần thực thi.
        arg: any, any,...
            Các format string cần truyền vào câu query
        Trả về:
        -------
        list
            Danh sách các dòng dữ liệu từ truy vấn.
        """
        try:
            self.cursor.execute(query, arg)
            self.conn.commit()

            affected_rows = self.cursor.rowcount

            # cursor.close()
            # conn.close()

            return affected_rows

        except pymysql.MySQLError as err:
            print(f"Database error: {err}")
            return None

    def call_stored_procedure(self, stored_proc_name, *params):
        """
        Kết nối đến MySQL và gọi một Stored Procedure bất kỳ.

        Tham số:
            - stored_proc_name (str): Tên stored procedure cần gọi.
            - *params: Các tham số truyền vào stored procedure.

        Ví dụ:
            call_stored_procedure("InsertTestData", "Alice", 22)
            call_stored_procedure("UpdateUserAge", 5, 30)
        """
        try:
            with self.cursor as cursor:
                cursor.callproc(stored_proc_name, params)
                result = cursor.fetchall()

                if result:
                    print(f"✅ Stored Procedure '{stored_proc_name}' thực thi thành công! Kết quả: {result}")
                else:
                    print(f"⚠ Stored Procedure '{stored_proc_name}' không trả về dữ liệu!")

            self.conn.commit()
        except pymysql.MySQLError as err:
            print(f"❌ Lỗi khi gọi stored procedure '{stored_proc_name}': {err}")

    def submit_order_transaction(self, orderInfo: Order):
        cursor = self.cursor
        orderDetails = orderInfo.orderItems
        try:
            #Tạo order mới
            orderQuery = "INSERT INTO `order` (EVoucherGiamGiaID, Payment, IsDineIn, TotalPrice, TotalAmount, EVoucherDiscount, Status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(orderQuery, (orderInfo.evoucherGiamGiaId, orderInfo.paymentMethod.value, orderInfo.isDineIn, orderInfo.totalPrice, orderInfo.totalAmount, orderInfo.evoucherDiscount, orderInfo.orderStatus.value))

            # Get last inserted order_id
            orderInfo.id = cursor.lastrowid
            print(orderInfo.id)

            # Insert order details
            orderDetailsQuery = """
                INSERT INTO `orderdetails` (OrderID, FoodItemID, EVoucherTangMonID, PromotionID, Amount, Price, Discount, Note) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            orderDetailsData = [(orderInfo.id, orderItem.foodItem.id, orderItem.evoucherTangMonId, orderItem.foodItem.promotion_id, orderItem.quantity, orderItem.foodItem.price, orderItem.foodItem.discount, orderItem.note) for orderItem in orderDetails]
            cursor.executemany(orderDetailsQuery, orderDetailsData)

            #Get ids of inserted orderDetails
            lengthOrderDetails = len(orderDetailsData)
            print(cursor.lastrowid)
            orderDetailsIDs = [cursor.lastrowid + i for i in range(lengthOrderDetails)]
            print(orderDetailsIDs)

            #Prepare data for OrderDetailsTopping and OrderDetailsVariant table after inserting all orderDetails
            orderDetailsToppingData = []
            orderDetailsVariantData = []
            for i in range(lengthOrderDetails):
                toppingList = orderDetails[i].toppingList
                variantList = orderDetails[i].variantList
                orderDetailsID = orderDetailsIDs[i]
                for topping in toppingList:
                    orderDetailsToppingData.append((orderDetailsID, topping.id, topping.price, topping.discount))
                print(orderDetailsToppingData)

                for variant in variantList:
                    orderDetailsVariantData.append((orderDetailsID, variant.id, variant.price, variant.additional_cost))
                print(orderDetailsVariantData)

            #Insert OrderDetailsTopping and OrderDetailsVariant
            if len(orderDetailsToppingData) > 0:
                orderDetailsToppingQuery = """
                                            INSERT INTO `orderdetailstopping` (OrderDetailsID, ToppingID, Price, Discount) 
                                            VALUES (%s, %s, %s, %s)
                                        """
                cursor.executemany(orderDetailsToppingQuery, orderDetailsToppingData)

            if len(orderDetailsVariantData) > 0:
                orderDetailsVariantQuery = """
                                            INSERT INTO `orderdetailsvariant` (OrderDetailsID, VariantID, Price, AdditionalCost) 
                                            VALUES (%s, %s, %s, %s)
                                        """
                cursor.executemany(orderDetailsVariantQuery, orderDetailsVariantData)

            # Commit transaction
            self.conn.commit()
            print("✅ Order, order details, orderDetailsTopping and orderDetailsVariant inserted successfully.")
        except pymysql.MySQLError as err:
            # Rollback transaction if anything fails
            self.conn.rollback()
            print(f"❌ Transaction failed: {err}")

        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()


class DatabaseManager:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def fetch_data(self, start_date=None, end_date=None, keyword=None, category=None):
        query = """
            SELECT f.CustomID AS MaMon, f.Name AS TenMon, c.Name AS NhomMon,
                   SUM(o.Amount) AS SoLuong, SUM(o.Discount) AS GiamGia,
                   SUM(o.Amount * (o.Price - o.Discount)) AS DoanhThu,
                   SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0)) AS LoiNhuan
            FROM fooditem f
            LEFT JOIN Category c ON c.ID = f.CategoryID
            LEFT JOIN orderdetails o ON f.ID = o.FoodItemID
            LEFT JOIN fooditem_history fh ON f.ID = fh.FoodItemID AND fh.IsEffective = TRUE
        """

        conditions = []
        params = []

        if start_date and end_date:
            conditions.append("o.CreateAt BETWEEN %s AND %s")
            params.extend([start_date, end_date])

        if keyword:
            conditions.append("f.Name LIKE %s")
            params.append(f"%{keyword}%")

        if category and category != "Tất cả nhóm món":
            conditions.append("c.Name = %s")
            params.append(category)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY f.CustomID, f.Name, c.Name;"
        print(query)

        try:
            conn = pymysql.connect(
                host=self.host, user=self.user, password=self.password,
                database=self.database, port=self.port, cursorclass=pymysql.cursors.DictCursor
            )
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
            conn.close()
            return result

        except pymysql.MySQLError as err:
            QMessageBox.critical(None, "Database Error", f"Lỗi truy vấn dữ liệu: {err}")
            return []

    def fetch_top2_products(self, start_date=None, end_date=None, keyword=None, category=None):
        if not start_date or not end_date:
            end_date = datetime.today().strftime("%Y-%m-%d")
            start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")

        conditions = []
        params = []

        # if start_date and end_date:
        #     conditions.append("o.CreateAt BETWEEN %s AND %s")
        #     params.extend([start_date, end_date])

        if keyword:
            conditions.append("f.Name LIKE %s")
            params.append(f"%{keyword}%")

        if category and category != "Tất cả nhóm món":
            conditions.append("EXISTS (SELECT 1 FROM Category c WHERE c.ID = f.CategoryID AND c.Name = %s)")
            params.append(category)

        # Ghép các điều kiện thành một chuỗi
        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        query = f"""
            WITH RECURSIVE date_series AS (
                SELECT %s AS NgayBan
                UNION ALL
                SELECT DATE_ADD(NgayBan, INTERVAL 1 DAY)
                FROM date_series
                WHERE NgayBan < %s
            ),
            Top2 AS (
                SELECT o.FoodItemID, f.Name, SUM(o.Amount) AS TotalSold
                FROM orderdetails o
                JOIN fooditem f ON o.FoodItemID = f.ID
                WHERE o.CreateAt BETWEEN %s AND %s
                {where_clause}
                GROUP BY o.FoodItemID, f.Name
                ORDER BY TotalSold DESC
                LIMIT 2
            )
            SELECT
                ds.NgayBan,
                t.FoodItemID,
                t.Name,
                COALESCE(SUM(o.Amount), 0) AS SoLuong,
                COALESCE(SUM(o.Amount * o.Price), 0) AS DoanhThu
            FROM date_series ds
            CROSS JOIN Top2 t
            LEFT JOIN orderdetails o
                ON t.FoodItemID = o.FoodItemID
                AND DATE(o.CreateAt) = ds.NgayBan
            GROUP BY ds.NgayBan, t.FoodItemID, t.Name
            ORDER BY ds.NgayBan;
        """

        # Thêm tham số vào params để đảm bảo an toàn khi thực thi SQL
        params = [start_date, end_date, start_date, end_date] + params

        # if conditions:
        #     query += " WHERE " + " AND ".join(conditions)
        # query_top_2 = f"""
        #     SELECT o.FoodItemID, f.Name, SUM(o.Amount) AS TotalSold
        #     FROM orderdetails o
        #     JOIN fooditem f ON o.FoodItemID = f.ID
        #     WHERE 1=1
        #     {conditions}
        #     GROUP BY o.FoodItemID, f.Name
        #     ORDER BY TotalSold DESC
        #     LIMIT 2
        # """
        #
        # query = f"""
        # SELECT
        #     o.CreateAt,
        #     t.FoodItemID,
        #     t.Name,
        #     COALESCE(SUM(o.Amount), 0) AS SoLuong,
        #     COALESCE(SUM(o.Amount * o.Price), 0) AS DoanhThu
        # FROM orderdetails o
        # INNER JOIN (query_top_2) t
        #     ON t.FoodItemID = o.FoodItemID
        # WHERE 1=1
        # {conditions}
        # GROUP BY ds.NgayBan, t.FoodItemID, t.Name
        # ORDER BY ds.NgayBan;
        # """

        try:
            with pymysql.connect(
                    host=self.host, user=self.user, password=self.password,
                    database=self.database, port=self.port, cursorclass=pymysql.cursors.DictCursor
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchall()
        except pymysql.MySQLError as err:
            QMessageBox.critical(None, "Database Error", f"Lỗi truy vấn dữ liệu: {err}")
            return []

    def fetch_categories(self):
        query = """
           SELECT DISTINCT c.ID, c.Name
           FROM Category c
           """

        try:
            with pymysql.connect(
                    host=self.host, user=self.user, password=self.password,
                    database=self.database, port=self.port, cursorclass=pymysql.cursors.DictCursor
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    categories = [row["Name"] for row in cursor.fetchall()]
                    print("Fetched categories:", categories)  # Log để kiểm tra
                    return categories
        except pymysql.MySQLError as err:
            QMessageBox.critical(None, "Database Error", f"Lỗi truy vấn nhóm món: {err}")
            return []
=======
        # finally:
        #     # Close the cursor and connection
        #     cursor.close()
        #     conn.close()

    def fetch_topgroup(self, FoodItemID):
       # Dựa vào ID --> Lấy danh sách nhóm topping
       query = """SELECT tg.ID, tg.Name
                   FROM toppinggroupfooditem tgfi
                   INNER JOIN toppinggroup tg ON tg.ID = tgfi.ToppingGroupID
                   WHERE tgfi.FoodItemID = %s;"""
       return self.fetch_data(query, FoodItemID)

    def fetch_each_top(self, ToppingGroupID):
        query = """SELECT t.ID,
                   fi.Name,
                   fh.Price, 
                   CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price * (1 - (p.Discount / 100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice,
                   fi.ImageURL
            FROM topping t
            INNER JOIN fooditem fi ON fi.ID = t.FoodItemID
            INNER JOIN fooditem_history fh ON fi.ID = fh.FoodItemID
            LEFT JOIN promotionfooditem pfi ON fi.ID = pfi.FoodItemID
            LEFT JOIN promotion p ON p.ID = pfi.PromotionID
            WHERE t.ToppingGroupID = %s;"""
        return self.fetch_data(query, ToppingGroupID)

    def fetch_all_toppings(self, FoodItemID):
        # Lấy toàn bộ danh sách topping dựa vào FoodItemID
        topping_groups = self.fetch_topgroup(FoodItemID)
        print(topping_groups)
        if not topping_groups:
            print("Không có nhóm topping nào cho món ăn này.")
            return []

        all_toppings = []
        for group in topping_groups:
            toppings = self.fetch_each_top(group['ID'])
            if toppings:
                all_toppings.extend(toppings)

        return all_toppings

    def fetch_variantgroup(self, FoodItemID):
        """Dụa vào ID --> Lấy hết các variant group"""
        query = """SELECT vg.ID, vg.Name, vg.IsRequired, vg.ViewType, vg.HasPrice
                          FROM variantgroupfooditem vgfi
                          INNER JOIN variantgroup vg ON vg.ID = vgfi.VariantGroupID
                          WHERE vgfi.FoodItemID = %s;"""
        return self.fetch_data(query, FoodItemID)

    def fetch_each_variant(self, VariantGroupID):
        # Dựa vào ID variant grouup --> Lấy hết các variant trong group đó
        query = """SELECT ID, Value, Price, AdditionalCost
                          FROM variant
                          WHERE variantGroupID = %s;"""
        return self.fetch_data(query, VariantGroupID)

    def fetch_all_variants(self, FoodItemID):
        # Lấy toàn bộ danh sách variant
        variant_groups = self.fetch_variantgroup(FoodItemID)
        if not variant_groups:
            return []

        all_variants = []
        for group in variant_groups:
            variants = self.fetch_each_variant(group['ID'])
            if variants:
                all_variants.extend(variants)

        return all_variants

    def update_customer_feedback(self, order_id, stars, reasons):
        reason_vote = "|".join(reasons) if reasons else ""
        query = "UPDATE `order` SET customer_vote = %s, reason_vote = %s WHERE ID = %s"
        return self.do_any_sql(query, stars, reason_vote, order_id)

if __name__ == "__main__":
    db = Database()
    query = """
                    SELECT fi.ID,
                           fi.Name,
                           fi.IsBestSeller,
                           fh.Price,
                           CAST(IF(pfi.FoodItemID IS NOT NULL, 
                                   IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), 
                                   fh.Price - p.Discount), 
                               fh.Price) AS UNSIGNED) AS DiscountedPrice,
                           fi.ImageURL,
                           pfi.PromotionID
                    FROM fooditem fi
                    INNER JOIN fooditem_history fh
                        ON fi.ID = fh.FoodItemId
                    LEFT JOIN promotionfooditem pfi
                        ON fi.ID = pfi.FoodItemID
                    LEFT JOIN (SELECT * FROM promotion WHERE IsEffective = True) p
                        ON p.ID = pfi.PromotionID
                    WHERE (fi.IsFulltime = True 
                           OR (fi.Days LIKE CONCAT('%%', CAST(WEEKDAY(current_timestamp) AS CHAR), '%%')
                           AND current_time BETWEEN fi.AvailableStartTime AND fi.AvailableEndTime))
                    AND fh.IsEffective = True;
                """
    items = db.fetch_data(query)
    print(items)


class Database_LoginApp:
    def __init__(self, host="34.80.75.195", user="dev", password="KTLTnhom4@", database="kioskapp", port=3306):
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            print("Kết nối thành công!")
        except pymysql.MySQLError as e:
            self.connection = None
            print(f"Lỗi kết nối MySQL: {e.args}")

    def fetch_all_orders(self, start_date=None, end_date=None):
        if self.connection is None:
            print("không thể thực hiện truy vấn vì kết nối database thất bại.")
            return None
        try:
            query = """
            SELECT Payment, TotalPrice, CreateAt
            FROM `order`
            """
            params = ()

            if start_date and end_date:
                if len(start_date) == 10:
                    start_date += " 00:00:00"
                if len(end_date) == 10:
                    end_date += " 23:59:59"

                query += " WHERE CreateAt BETWEEN %s AND %s"
                params = (start_date, end_date)

            query += " ORDER BY CreateAt DESC;"
            self.cursor.execute(query, params)
            all_orders = self.cursor.fetchall()
            return all_orders
        except pymysql.MySQLError as e:
            print(f"Lỗi truy vấn MySQL: {e.args}")
            return None

