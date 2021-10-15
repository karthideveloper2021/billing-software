import sqlite3

class connectData:
    def __init__(self):
        self.itemConn=sqlite3.connect("data.db")
        self.itemCursor=self.itemConn.cursor()
        self.itemCursor.execute("CREATE TABLE IF NOT EXISTS item(item_number INTEGER PRIMARY KEY,item_name VARCHAR(100),item_rate FLOAT,item_price FLOAT,item_details VARCHAR(200))")

    def addItemProcess(self,itemNo,itemName,itemRate,itemPrice,itemDetails):
        
        self.itemCursor.execute("INSERT INTO item VALUES(?,?,?,?,?)",(itemNo,itemName,itemRate,itemPrice,itemDetails))
        self.itemConn.commit()
    
    def getItemProcess(self):
        self.itemCursor.execute("SELECT * FROM item")
        self.itemsData=self.itemCursor.fetchall()

if __name__=="__main__":
    #testing purpose
    
    print('database')
    c=connectData()
    c.getItemProcess()
    print(c.itemsData)