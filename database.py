import sqlite3

class connectData:
    def __init__(self):
        self.itemConn=sqlite3.connect("data.db")
        self.itemCursor=self.itemConn.cursor()
        self.itemCursor.execute("CREATE TABLE IF NOT EXISTS item(item_number INTEGER PRIMARY KEY,item_name VARCHAR(100),item_price FLOAT,item_details VARCHAR(200))")
        self.initializeCustomerBill()

    def initializeCustomerBill(self):
        self.itemCursor.execute("CREATE TABLE IF NOT EXISTS customerBill(name VARCHAR(10),items VARCHAR(1000),billtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)")

    def addItemProcess(self,itemNo,itemName,itemPrice,itemDetails):
        
        self.itemCursor.execute("INSERT INTO item VALUES(?,?,?,?)",(itemNo,itemName,itemPrice,itemDetails))
        self.itemConn.commit()
    
    def getItemProcess(self):
        self.itemCursor.execute("SELECT * FROM item")
        self.itemsData=self.itemCursor.fetchall()
    
    def getItemSpecific(self,itemNO):
        self.itemCursor.execute("SELECT * FROM item WHERE item_number={ItemNo}".format(ItemNo=itemNO))
        self.itemSpecificRow=self.itemCursor.fetchone()
        return self.itemSpecificRow
        
    def customerBillCopy(self,billname,billitems):
        self.itemCursor.execute("INSERT INTO customerBill(name,items) values(?,?)",(billname,billitems))
        self.itemConn.commit()

if __name__=="__main__":
    #testing purpose
    
    print('database')
    c=connectData()
    print(c.getItemSpecific(1001))
