import mysql.connector

class Connector:
    def __init__(self):
        self.server="34.101.167.101"#127.0.0.1
        self.port=3306
        self.database="kioskapp"
        self.username="dev"
        self.password="12345678x@X"
        self.conn = mysql.connector.connect(
            host=self.server,
            port=self.port,
            database=self.database,
            user=self.username,
            password=self.password
        )


    def query(self, sql, val_input=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, val_input)
        return cursor



class DataBase(Connector):
    def checkVoucherGiamGia(self, voucher):
        sql = f"""
        SELECT ID 
	  ,EvoucherGiamGiaID
        FROM evouchergiamgialist
        WHERE Value = %s
        AND IsUsed = False 
        LIMIT 1"""
        input = (voucher,)
        cursor = self.query(sql, input)
        evou = cursor.fetchone()
        cursor.close()
        return evou
    def checkisEffectiveGiamGia(self, voucher):
        evou = self.checkVoucherGiamGia(voucher)
        if evou is not None:
            evouchergiamgiaID = evou[1]
            sql = f"""
            SELECT evgg.ID
                  ,evgg.Discount #Giá trị giảm
                  ,evgg.IsPercent #Flag giảm theo phần trăm
                  ,evgg.MinimumPrice #Hoá đơn ít nhất bao nhiêu thì mới được áp mã giảm giá
                  ,evgg.MaximumDiscount #Hoá đon được giảm nhiều nhất là bao nhiêu
            FROM evouchergiamgia evgg
            INNER JOIN evoucher ev
            ON ev.ID = evgg.EVoucherID
            WHERE evgg.ID = %s
            AND ev.IsEffective = True"""
            input = (evouchergiamgiaID,)
            cursor = self.query(sql, input)
            vou_giamgia = cursor.fetchone()
            cursor.close()
            if vou_giamgia is not None:
                return vou_giamgia
            else:
                return "Rất tiếc! Mã voucher đã hết hạn sử dụng."

    def checkisUsedTangMon(self, voucher):
        sql = f"""
        SELECT ID
              ,EVoucherTangMonID
              ,IsUsed
        FROM evouchertangmonlist
        WHERE Value = %s
        AND IsUsed = False #Kiểm tra voucher đã sử dụng chưa"""
        input = (voucher,)
        cursor = self.query(sql, input)
        evou_tangmon = cursor.fetchone()
        cursor.close()
        return evou_tangmon
    def checkIsEffectiveTangMon(self, voucher):
        evou = self.checkisUsedTangMon(voucher)
        if evou is not None:
            evouchertangmonID = evou[1]
            sql = f"""
            SELECT fi.ID
                  ,fi.Name
                  ,fi.ImageURL
                  ,fih.Price
                  ,0 AS DiscountedPrice 
                  ,evtm.ID AS EvoucherTangMonID
                  ,evtm.Amount 
                  ,evtm.MinimumPrice 
            FROM evouchertangmon evtm
            INNER JOIN evoucher ev
            ON ev.ID = evtm.EVoucherID
            INNER JOIN fooditem fi
            ON fi.ID = evtm.FoodItemID
            INNER JOIN fooditem_history fih
            ON fi.ID = fih.FoodItemID
            WHERE evtm.ID = %s
            AND ev.IsEffective = TRUE 
            AND fih.IsEffective = TRUE"""
            input = (evouchertangmonID,)
            cursor = self.query(sql, input)
            vou_tangmon = cursor.fetchone()
            if vou_tangmon is not None:
                cursor.close()
                return vou_tangmon
            return "Rất tiếc! Mã voucher đã hết hạn sử dụng."

    def responseVoucher(self, voucher, totaltemp):
        if voucher.strip() == "":
            return None
        warn = "Bạn không đủ điều kiện để áp dụng voucher này."
        "TH Giám giá"
        evoug = self.checkisEffectiveGiamGia(voucher)
        if evoug is not None:
            if type(evoug) is str:
                return evoug
            if totaltemp > evoug[3]:
                if evoug[2] == 1:
                    "Giảm giá theo phần trăm"
                    total = totaltemp*(1-evoug[1]/100)
                else:
                    "Giảm giá không theo phần trăm"
                    total = totaltemp - evoug[1]
                if total > evoug[4]:
                    "Giới hạn số tiền giảm giá"
                    total = totaltemp - evoug[4]
                return total
            else:
                return warn
        "TH Tặng món"
        evout = self.checkIsEffectiveTangMon(voucher)
        if evout is not None:
            if type(evout) is str:
                return evout
            if totaltemp > evout[7]:
                return evout
            else:
                return warn
        "TH sai voucher"
        if evout is None and evoug is None:
            return f"Rất tiếc! Mã voucher không hợp lệ hoặc đã bị sử dụng"
class OrderItem:
    def __init__(self, id, name, imageurl, topping, price, quantity, isdeleted, isfree = 0):
        self.id = id
        self.name = name
        self.imageurl = imageurl
        self.topping = topping
        self.price = price
        self.quantity = quantity
        self.isdeleted = isdeleted
        self.isfree = isfree
    def __str__(self):
        info = f"{self.id}\t{self.name}\t{self.imageurl}\t{self.topping}\t{self.price}\t{self.quantity}\t{self.isdeleted}"
        return info
class ListOrderItem:
    def __init__(self):
        self.listorders = []
    def addItem(self, item):
        self.listorders.append(item)
    def listOrders(self):
        return self.listorders
    def getItemById(self, i):
        return self.listorders[i]
    def countListOrders(self):
        return len(self.listorders)
    def totalPrice(self):
        totalprice = 0
        for item in self.listorders:
            if item.isdeleted == 0 and item.isfree ==0:
                totalprice = totalprice+ item.price*item.quantity
        return totalprice
    def countListOrderNotDeleted(self):
        numb = 0
        for item in self.listorders:
            if item.isdeleted == 0:
                numb += 1
        return numb
    def deleteDuplicateOrder(self):
        l = len(self.listorders)
        for i in range(l):
            for j in range(i+1, l):
                if self.listorders[j] == self.listorders[i]:
                    self.listorders.pop(j)
    def findFreeItem(self):
        for item in self.listorders:
            if item.isfree == 1:
                return item
        return None

"""TEST"""
item1 = OrderItem(1, "Trà Đào", "../resources/images/tra.png", "", 19000, 5, 0)
item2 = OrderItem(2, "Bánh tráng trộn", "../resources/images/tra.png", "", 20000, 3, 0)
item3 = OrderItem(3, "Bánh tráng trộn", "../resources/images/tra.png", "", 20000, 3, 0)
item4 = OrderItem(4, "Bánh tráng trộn", "../resources/images/tra.png", "", 20000, 3, 0)
item5 = OrderItem(2, "Trà đào", "../resources/images/traxoai.png", "", 19000, 2, 0)
listorders = ListOrderItem()
listorders.addItem(item1)
listorders.addItem(item2)
listorders.addItem(item3)
listorders.addItem(item4)
# print(listorders.getItemById(2))
# print(listorders.totalPrice())






kiosk = DataBase()
voucher = 'TESTTANGMON01'
voucher1 = 'TESTGIAMGIA01'
evou = kiosk.responseVoucher(voucher, 290000)
evou1 = kiosk.responseVoucher(voucher1, 290000)

# print(evou)
# print(evou1)




