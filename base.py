from tkinter import *  
from tkinter import ttk,messagebox
from database import connectData
import time

class mainLayout:
    def __init__(self,main):
        self.master=main
        self.header()
        self.content()
        self.menu()
                
        
    def header(self):
        self.head=header(self.master)

    def content(self):
        self.masterFrame=Frame(self.master,bg="red")
        self.masterFrame.pack(fill=BOTH,expand=True)
        self.home()

    def menu(self):
        self.menuBar=Menu(self.master)
        self.master.config(menu=self.menuBar)       

        self.dashboardMenu=Menu(self.menuBar,tearoff=OFF)
        self.dashboardMenu.add_command(label="Home",command=self.home)
        self.dashboardMenu.add_command(label="Quit",command=self.quitMessageBox)

        self.dataMenu=Menu(self.menuBar,tearoff=OFF)
        self.dataMenu.add_command(label="Data",command=self.data)
        self.dataMenu.add_command(label="Analysis",command=self.analysis)

        self.menuBar.add_cascade(label="Dashboard",menu=self.dashboardMenu)
        self.menuBar.add_cascade(label="Database",menu=self.dataMenu)
        self.menuBar.add_cascade(label="About",command=None)
        

    def home(self):
        self.destroyFramesWidgets()
        self.head.updateTitle("BILLING")
        getDataLayout(self.masterFrame)

    def data(self):
        self.destroyFramesWidgets()
        self.head.updateTitle("DATABASE")
        self.insertObj=insertDataLayout(self.masterFrame)
        

    def analysis(self):
        self.destroyFramesWidgets()
        self.head.updateTitle("ANALYSIS")
        

    def destroyFramesWidgets(self):
        for widget in self.masterFrame.winfo_children():
            widget.destroy()

    def quitMessageBox(self):

        if messagebox.askokcancel("Confirm","Are you sure?"):
            self.master.quit()

class header:
    def __init__(self,main):
        self.headerFrame=Frame(main,bg="green")
        self.headerFrame.pack(fill=X)
        self.fontcolor=["red","black","green","yellow","green","brown","pink","blue"]
        self.clock()
        self.mainTitle()
        

    def clock(self):

        self.timeLabel=Label(self.headerFrame,font=("",18,""),bg="black",fg="white")
        self.timeLabel.pack(side=RIGHT,padx=10,pady=5)
        self.updateTime()
        
    def updateTime(self):

        self.timeLabel.config(text=time.strftime("%I")+":"+time.strftime("%M")+":"+time.strftime("%S")+" "+time.strftime("%p"))
        self.timeLabel.after(1000,self.updateTime)

    def mainTitle(self):
        self.title=Label(self.headerFrame,font=("bauhaus 93",28,""))
        self.title.pack(side=LEFT,padx=10)
        self.colorTitle(0)
        
    def updateTitle(self,titleText):
        self.title.config(text=titleText)
    
    def colorTitle(self,colorIndex):
        self.title.config(fg=self.fontcolor[colorIndex])
        if colorIndex==len(self.fontcolor)-1:
            colorIndex=0
        else:
            colorIndex+=1
        self.title.after(800,self.colorTitle,colorIndex) 

class getDataLayout:
    def __init__(self,main):
        self.getFrame=Frame(main)
        self.getFrame.pack(side=LEFT,anchor=N,padx=100,pady=100)
        self.treeViewFrame=Frame(main)
        self.treeViewFrame.pack(side=RIGHT,padx=20)
        self.billingInput()
        self.billingList()

    
    def billingInput(self):
        
        self.inputFont=("",18,"")
        self.LabelFont=("impact",15,"")

        self.itemLabel=Label(self.getFrame,text="ITEM NO",font=self.LabelFont)
        self.itemNO=Entry(self.getFrame,font=self.inputFont)
        self.quantityLabel=Label(self.getFrame,text="QUANTITY",font=self.LabelFont)
        self.quantity=Entry(self.getFrame,font=self.inputFont)
        self.add=Button(self.getFrame,text="ADD",font=self.LabelFont,width=10)

        self.itemLabel.pack(pady=10)
        self.itemNO.pack(pady=10,padx=20)
        self.quantityLabel.pack(pady=10,padx=20)
        self.quantity.pack(pady=10,padx=20)
        self.add.pack(pady=10)
        
        self.itemNO.focus_set()
    
    def billingList(self):
        

        self.itemsList=ttk.Treeview(self.treeViewFrame)
        self.itemsList.pack()

        self.itemsList['columns']=["sno","no","name","quantity","rate","price"]

        self.itemsList.heading("#0")
        self.itemsList.heading("sno",text="S.NO")
        self.itemsList.heading("no",text="ITEMS NO")
        self.itemsList.heading("name",text="NAME")
        self.itemsList.heading("quantity",text="QUANTITY")
        self.itemsList.heading("rate",text="RATE")
        self.itemsList.heading("price",text="PRICE")

        self.itemsList.column("#0",width=0,stretch=OFF)
        self.itemsList.column("sno",width=60,minwidth=50)
        self.itemsList.column("no",width=120,minwidth=90)
        self.itemsList.column("name",width=170,minwidth=160)
        self.itemsList.column("quantity",width=120,minwidth=90)
        self.itemsList.column("rate",width=170,minwidth=50)
        self.itemsList.column("price",width=170,minwidth=50)
        
class insertDataLayout:
    def __init__(self,main):
        self.putFrame=Frame(main)
        self.putFrame.pack(side=LEFT,padx=100,pady=100,anchor=N)

        self.listFrame=Frame(main)
        self.listFrame.pack(side=RIGHT,padx=100,anchor=CENTER)

        self.conDat=connectData()
        self.inputBox()
        self.listView()
    

    def inputBox(self):
        self.inputFont=("",18,"")
        self.LabelFont=("",15,"")
        self.entryStyle={"highlightcolor":"blue",
                          "highlightthickness":"1"}

        self.NoLabel=Label(self.putFrame,text="Item no",font=self.LabelFont)
        self.NameLabel=Label(self.putFrame,text="Name",font=self.LabelFont) 
        self.RateLabel=Label(self.putFrame,text="Rate",font=self.LabelFont)
        self.PriceLabel=Label(self.putFrame,text="Price",font=self.LabelFont)
        self.DetailsLabel=Label(self.putFrame,text="Details",font=self.LabelFont)

        self.itemNo=Entry(self.putFrame,font=self.inputFont,highlightcolor="blue",highlightthickness=1)
        self.itemName=Entry(self.putFrame,font=self.inputFont,border=0)
        self.itemRate=Entry(self.putFrame,font=self.inputFont)
        self.itemPrice=Entry(self.putFrame,font=self.inputFont)
        self.itemDetails=Text(self.putFrame,font=self.inputFont,width=20,height=5)
        

        self.add=Button(self.putFrame,text="ADD",width=10,relief=FLAT,command=self.addItem)
        self.reset=Button(self.putFrame,text="RESET",width=10,relief=FLAT,command=self.deleteInput)

        self.NoLabel.grid(row=0,column=0,padx=10,pady=10,sticky=W)
        self.itemNo.grid(row=0,column=1,padx=10,pady=10)
        self.NameLabel.grid(row=1,column=0,padx=10,pady=10,sticky=W)
        self.itemName.grid(row=1,column=1,padx=10,pady=10)
        self.RateLabel.grid(row=2,column=0,padx=10,pady=10,sticky=W)
        self.itemRate.grid(row=2,column=1,padx=10,pady=10)
        self.PriceLabel.grid(row=3,column=0,padx=10,pady=10,sticky=W)
        self.itemPrice.grid(row=3,column=1,padx=10,pady=10)
        self.DetailsLabel.grid(row=4,column=0,padx=10,pady=10,sticky=W)
        self.itemDetails.grid(row=4,column=1,padx=10,pady=10)
        self.add.grid(row=5,column=0,padx=10,pady=10)
        self.reset.grid(row=5,column=1,padx=10,pady=10,sticky=W)

    
       
    def addItem(self):

        if (self.itemNo.get()=="") or (self.itemName.get()=="") or (self.itemNo.get()=="" and self.itemName.get()==""):
            messagebox.showerror("Warning","Missing input(s)")

        else:
            self.conDat.addItemProcess(self.itemNo.get(),self.itemName.get(),self.itemRate.get(),self.itemPrice.get(),self.itemDetails.get(0.1,END))
            self.deleteInput()

            self.itemTree.delete(*self.itemTree.get_children())
            self.insertTreeDatabase()

    def deleteInput(self):
        self.itemNo.delete(0,END)
        self.itemName.delete(0,END)
        self.itemRate.delete(0,END)
        self.itemPrice.delete(0,END)
        self.itemDetails.delete(0.1,END)
      
        
    def listView(self):
        
        self.itemTree=ttk.Treeview(self.listFrame)
        self.itemTree.pack()
    
        self.itemTree['columns']=("serial","no","name","rate","quantity","price")

        self.itemTree.column("#0",width=1)
        self.itemTree.column("serial",width=60,minwidth=50,stretch=NO)
        self.itemTree.column("no",width=100,minwidth=50)
        self.itemTree.column("name",width=260,minwidth=200)
        self.itemTree.column("rate",width=100,minwidth=70)
        self.itemTree.column("quantity",width=100,minwidth=70)
        self.itemTree.column("price",width=100,minwidth=70)

        self.itemTree.heading("#0",text="")
        self.itemTree.heading("serial",text="S.No")
        self.itemTree.heading("no",text="ITEM.NO")
        self.itemTree.heading("name",text="ITEM NAME")
        self.itemTree.heading("rate",text="RATE")
        self.itemTree.heading("quantity",text="QUANTITY")
        self.itemTree.heading("price",text="PRICE")

        self.insertTreeDatabase()

    def insertTreeDatabase(self):

        #self.itemTree.insert(parent="",index=END,iid=0,values=("1","2","3","4","5","6"))
        self.conDat.getItemProcess()
        sNO=0
        for item in self.conDat.itemsData:
            self.itemTree.insert(parent="",index=END,iid=sNO,text="parent",values=(sNO,item[0],item[1],item[2],item[3]))
            sNO+=1


if __name__ == "__main__":
    base=Tk()
    base.state("zoomed")
    mainLayout(base)
    base.mainloop()