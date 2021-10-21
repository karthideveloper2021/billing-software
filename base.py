from tkinter import *  
from tkinter import ttk,messagebox
from style import stylesheet
import database
import time
from configparser import ConfigParser

class mainLayout:
    def __init__(self,main):
        self.master=main
        self.menu()
        self.header()
        self.footer()
        self.content()
        
        
        
                
        
    def header(self):
        self.head=header(self.master)

    def content(self):
        self.contentFrame=Frame(self.master,bg="red")
        self.contentFrame.pack(fill=BOTH,expand=True)
        self.contentFrame.rowconfigure(0,weight=1)
        self.contentFrame.columnconfigure(0,weight=1)

        self.getObj=getDataLayout(self.contentFrame)
        self.insertObj=insertDataLayout(self.contentFrame)
        self.analysisObj=analysisLayout(self.contentFrame)
        self.home()

    def footer(self):
        self.foot=Frame(self.master)
        self.foot.pack(side=BOTTOM)
        Label(self.foot,text="This is footer").pack()

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
        self.getObj.master.tkraise()
        self.head.updateTitle("BILLING")

    def data(self):
        self.insertObj.master.tkraise()
        self.head.updateTitle("DATABASE")
        
        

    def analysis(self):
        self.analysisObj.master.tkraise()
        self.head.updateTitle("ANALYSIS")
        

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
        
        def updateTime():

            self.timeLabel.config(text=time.strftime("%I:%M:%S %p"))
            self.timeLabel.after(1000,updateTime)
        updateTime()

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
        self.master=Frame(main)
        self.master.grid(row=0,column=0,sticky=NSEW)
        
        self.initialize()
        self.billingInput()
        self.billingList()
        self.keyBindings()

        
    
    def billingInput(self):
        
        self.getFrame=Frame(self.master,bg="red")
        self.getFrame.pack(side=LEFT,anchor=N,padx=100)

        self.initializeValidate()

        self.inputFont=("",18,"")
        self.LabelFont=("impact",18,"")
        self.itemLabel=Label(self.getFrame,text="ITEM NO",**stylesheet().billingLabel)
        self.itemNO=Entry(self.getFrame,**stylesheet().billingEntry,validate="key",validatecommand=(self.entryIntReg,"%P"))
        self.itemNameLabel=Label(self.getFrame,text="ITEM NAME",**stylesheet().billingLabel)
        self.itemName=Entry(self.getFrame,**stylesheet().billingEntry)
        self.quantityLabel=Label(self.getFrame,text="QUANTITY",**stylesheet().billingLabel)
        self.quantity=Entry(self.getFrame,**stylesheet().billingEntry,validate="key",validatecommand=(self.entryIntReg,"%P"))
        self.add=Button(self.getFrame,text="ADD",font=self.LabelFont,width=10,command=self.addCart)
        self.reset=Button(self.getFrame,text="RESET",font=self.LabelFont,width=10)

        self.itemLabel.pack(pady=10)
        self.itemNO.pack(pady=10,padx=20)
        self.itemNameLabel.pack(pady=10,padx=20)
        self.itemName.pack(pady=10,padx=20)
        self.quantityLabel.pack(pady=10,padx=20)
        self.quantity.pack(pady=10,padx=20)
        self.add.pack(pady=10)
        self.reset.pack(pady=10)
        
        self.itemNO.focus_set()

        self.customerDetails()

        self.print=Button(self.getFrame,text="PRINT",font=self.LabelFont,command=self.billingUpload)
        self.print.pack(pady=10)
    
        print(self.itemNO.winfo_class())

        self.search=Listbox(self.getFrame,font=self.itemName.cget('font'),height=0)

    def searchListPlace(self):
        
        self.search.place(x=self.itemName.winfo_x(),y=self.itemName.winfo_y()+2*self.itemName.cget('width'))
        itemsData=self.billingObj.getItemProcessItemNames()
        print(itemsData)
        for items in itemsData:
            if self.itemName.get().lower() in items[0].lower():
                self.search.insert(END,items[0])

    def billingList(self):
        
        self.billingListFrame=Frame(self.master,bg="green")
        self.billingListFrame.pack(side=RIGHT,padx=20,fill=Y)

        self.billingInfo()

        self.itemsList=ttk.Treeview(self.billingListFrame)
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
        self.itemsList.column("sno",width=60,minwidth=50,anchor=CENTER)
        self.itemsList.column("no",width=120,minwidth=90,anchor=CENTER)
        self.itemsList.column("name",width=270,minwidth=160,anchor=CENTER)
        self.itemsList.column("quantity",width=120,minwidth=90,anchor=CENTER)
        self.itemsList.column("rate",width=120,minwidth=50,anchor=E)
        self.itemsList.column("price",width=120,minwidth=50,anchor=E)

        self.billingCheckout() 
        

    def billingInfo(self):
        self.billingNumNext()
        self.billingInfoFrame=Frame(self.billingListFrame,bg="blue")
        self.billingInfoFrame.pack(fill=X)

        self.title=Label(self.billingInfoFrame,text="BILLING")
        self.title.pack()

        self.billNoLabel=Label(self.billingInfoFrame,text="BILL NO")
        self.billNoLabel.pack(side=LEFT,padx=10)

        self.billNo=Label(self.billingInfoFrame,text=self.billNum)
        self.billNo.pack()
        

    def billingNumNext(self):
        date=time.strftime("%d/%m/%Y")
        self.customerCount=int(self.parserControl.get('customerDetails','customerCount'))
        checkDate=self.parserControl.get('customerDetails','date')

        if checkDate==date:
            self.customerCount+=1
        else:
            self.customerCount=1
            self.parserControl.set('customerDetails','date',date)
        self.parserControl.set('customerDetails','customerCount',str(self.customerCount))
                    
        self.billNum="B"+date[:2]+time.strftime("%w")+str(self.customerCount)

    def configWriting(self):
        with open("settings.ini","w") as settingsFile:
            self.parserControl.write(settingsFile)

    def billingCheckout(self):
        self.checkoutFrame=Frame(self.billingListFrame,bg="brown")
        self.checkoutFrame.pack(side=RIGHT,anchor=N,padx=50,pady=10)

        self.totalLabel=Label(self.checkoutFrame,text="TOTAL",**stylesheet().billingListLabel)
        self.totalLabel.grid(row=0,column=0)

        self.totalPriceLabel=Label(self.checkoutFrame,text=self.totalPrice,**stylesheet().billingListLabel)
        self.totalPriceLabel.grid(row=0,column=1,padx=22)

    def billingUpload(self):
        
        for line in self.itemsList.get_children():               
            value= self.itemsList.item(line)['values']
            self.CartItemsDic[value[1]]=value[3]
        self.billItems=str(self.CartItemsDic)
        self.billingObj.customerBillCopy(self.billNum,self.billItems)
        self.CartItemsDic.clear()
        self.configWriting()
        self.billingNumNext()
        self.billNo.config(text=self.billNum)
        
    def updateTotalinfo(self):
        self.totalPrice=0.0
        for line in self.itemsList.get_children():
            self.totalPrice+=float(self.itemsList.item(line)['values'][-1])
        self.totalPriceLabel.config(text=self.totalPrice)   

    def addCart(self):


        for entryWidget in self.getFrame.winfo_children():
            if entryWidget.winfo_class()=="Entry":
                if entryWidget.get()=="":
                    messagebox.showwarning("Error","Invalid input")
                    break

        else:
            itemdetails=self.billingObj.getItemSpecific(self.itemNO.get())
            if self.add.cget('text')=="ADD":
                self.totalAmt=float(self.quantity.get())*itemdetails[2]
                self.itemsList.insert(parent="",index=END,iid=self.totalItems,values=(self.totalItems+1,itemdetails[0],itemdetails[1],self.quantity.get(),itemdetails[2],self.totalAmt))
                self.totalItems+=1   
            elif self.add.cget('text')=="UPDATE":
                self.totalAmt=float(self.quantity.get())*itemdetails[2]
                print(self.totalAmt)
                for line in self.itemsList.get_children():               
                    value= self.itemsList.item(line)['values']
                    if int(self.itemNO.get())==value[1]:
                        self.itemsList.item(line,values=(value[0],itemdetails[0],itemdetails[1],self.quantity.get(),itemdetails[2],self.totalAmt))
                        break
            self.updateTotalinfo()
            self.deleteInputs()

    def deleteInputs(self):
        self.itemNO.delete(0,END)
        self.itemName.delete(0,END)
        self.quantity.delete(0,END)
        self.itemNO.focus_set()

    def initialize(self):
        self.billingObj=database.connectData()
        self.totalItems=0
        self.totalPrice=0.0
        self.customerCount=0
        self.CartItemsDic={}
        self.parserControl=ConfigParser()
        self.parserControl.read("settings.ini")

    def customerDetails(self):
        
        self.comboFont=("lucida fax",14,"")

        self.customerDetailsFrame=Frame(self.getFrame)
        self.customerDetailsFrame.pack(pady=50)

        self.cusNameLabel=Label(self.customerDetailsFrame,text="CUSTOMER NAME",**stylesheet().billingLabel)
        self.cusName=Entry(self.customerDetailsFrame,**stylesheet().customerEntry)
        self.payModeLabel=Label(self.customerDetailsFrame,text="PAYMENT",**stylesheet().billingLabel)
        
        self.paySelect=StringVar()
        self.payList=["CASH","CARD","UPI"]
        self.paySelect.set(self.payList[0])
        self.payMode=OptionMenu(self.customerDetailsFrame,self.paySelect,*self.payList)
        self.payMode.config(**stylesheet().customerOption)
        self.payModeMenu=self.customerDetailsFrame.nametowidget(self.payMode.menuname)
        self.payModeMenu.config(**stylesheet().customerOption)

        self.cusNameLabel.grid(row=0,column=0,pady=5,padx=10)
        self.cusName.grid(row=0,column=1,pady=5,padx=10)
        self.payModeLabel.grid(row=1,column=0,pady=5,padx=10)
        self.payMode.grid(row=1,column=1,pady=5,padx=10,sticky=W)

    def keyBindings(self):

        def itemNocheck(event):
            self.quantity.focus_set()
            #if self.itemNO.get() in self.CartItemsDic.keys():
            for line in self.itemsList.get_children():               
                value= self.itemsList.item(line)['values']
                if int(self.itemNO.get())==value[1]:
                    self.add.config(text="UPDATE")
                else:
                    self.add.config(text="ADD")
                
        def addingProcess(event):
            self.addCart()
            self.add.config(text="ADD")
        
        def searchProcess(event):
            self.search.delete(0,END)
            if self.itemName.get()=="" or event.keysym=="Escape":
                self.search.place_forget()
            else:
                self.searchListPlace()
        
        def updateSearch(event):
            print(event.widget.curselection()[0])
            itemData=self.billingObj.getItemName(event.widget.get(event.widget.curselection()[0]))
            print(itemData)
            self.deleteInputs()
            self.itemNO.insert(0,itemData[0])
            self.itemName.insert(0,itemData[1])
            self.search.place_forget()
            self.quantity.focus_set()
        
        def listItemSelection(event):
            key=event.keysym
            if key=="Up":
                if event.widget.curselection()[0]==0:
                    self.itemName.focus_set()
            elif key=="Down":
                self.search.focus_set()
                self.search.selection_set(0)
                self.search.selection_anchor(0)


        def listCursorSelection(event):

            totalIndex=len(self.search.get(0,END))
            self.search.selection_clear(0,END)
            for i in range(0,totalIndex):
                element=self.search.bbox(i)
                if element[1]<event.y and (element[1]+element[3])>event.y:
                    self.search.selection_set(i)
                    break

        self.itemNO.bind("<Tab>",itemNocheck)
        self.itemNO.bind("<Return>",itemNocheck)
        self.quantity.bind("<Return>",addingProcess)

        self.itemName.bind("<KeyRelease>",searchProcess)
        self.itemName.bind("<Down>",listItemSelection)
        #self.search.bind("<<ListboxSelect>>",updateSearch)
        self.search.bind("<Return>",updateSearch)
        self.search.bind("<Button-1>",updateSearch)
        self.search.bind("<Motion>",listCursorSelection)
        self.search.bind("<Up>",listItemSelection)

    def initializeValidate(self):
        def intCallBack(value):
                if str.isdigit(value) or value=="":
                    return True
                else:
                    return False
        self.entryIntReg=self.getFrame.register(intCallBack)
        
class insertDataLayout:
    def __init__(self,main):

        self.master=Frame(main)
        #self.master.place(x=0,y=0)
        self.master.grid(row=0,column=0,sticky=NSEW)       

        self.initializeDb()
        self.inputBox()
        self.listView()

        
    def initializeDb(self):
        self.conDat=database.connectData()
 
    def inputBox(self):
        self.putFrame=Frame(self.master)
        self.putFrame.pack(side=LEFT,padx=100,pady=100,anchor=N)

        self.inputFont=("",18,"")
        self.LabelFont=("",15,"")
        self.entryStyle={"highlightcolor":"blue",
                          "highlightthickness":"1"}

        self.NoLabel=Label(self.putFrame,text="Item no",font=self.LabelFont)
        self.NameLabel=Label(self.putFrame,text="Name",font=self.LabelFont) 
        self.PriceLabel=Label(self.putFrame,text="Price",font=self.LabelFont)
        self.DetailsLabel=Label(self.putFrame,text="Details",font=self.LabelFont)

        self.itemNo=Entry(self.putFrame,font=self.inputFont,highlightcolor="blue",highlightthickness=1)
        self.itemName=Entry(self.putFrame,font=self.inputFont,border=0)
        self.itemPrice=Entry(self.putFrame,font=self.inputFont)
        self.itemDetails=Text(self.putFrame,font=self.inputFont,width=20,height=5)
        

        self.add=Button(self.putFrame,text="ADD",width=10,relief=FLAT,command=self.addItem)
        self.reset=Button(self.putFrame,text="RESET",width=10,relief=FLAT,command=self.deleteInput)

        self.NoLabel.grid(row=0,column=0,padx=10,pady=10,sticky=W)
        self.itemNo.grid(row=0,column=1,padx=10,pady=10)
        self.NameLabel.grid(row=1,column=0,padx=10,pady=10,sticky=W)
        self.itemName.grid(row=1,column=1,padx=10,pady=10)
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
            self.conDat.addItemProcess(self.itemNo.get(),self.itemName.get(),self.itemPrice.get(),self.itemDetails.get(0.1,END))
            self.deleteInput()

            self.itemTree.delete(*self.itemTree.get_children())
            self.insertTreeDatabase()

    def deleteInput(self):
        self.itemNo.delete(0,END)
        self.itemName.delete(0,END)
        self.itemPrice.delete(0,END)
        self.itemDetails.delete(0.1,END)
      
        
    def listView(self):
        self.listFrame=Frame(self.master)
        self.listFrame.pack(side=RIGHT,padx=100,anchor=CENTER)

        self.itemTree=ttk.Treeview(self.listFrame)
        self.itemTree.pack()
    
        self.itemTree['columns']=("serial","no","name","price","details")

        self.itemTree.column("#0",width=0,stretch=OFF)
        self.itemTree.column("serial",width=60,minwidth=50,stretch=NO)
        self.itemTree.column("no",width=100,minwidth=50)
        self.itemTree.column("name",width=260,minwidth=200)
        self.itemTree.column("price",width=100,minwidth=70)
        self.itemTree.column("details",width=100,minwidth=70)

        self.itemTree.heading("#0",text="")
        self.itemTree.heading("serial",text="S.No")
        self.itemTree.heading("no",text="ITEM.NO")
        self.itemTree.heading("name",text="ITEM NAME")
        self.itemTree.heading("price",text="PRICE")
        self.itemTree.heading("details",text="DETAILS")


        self.insertTreeDatabase()

    def insertTreeDatabase(self):

        #self.itemTree.insert(parent="",index=END,iid=0,values=("1","2","3","4","5","6"))
        itemsData=self.conDat.getItemProcess()
        sNO=0
        for item in itemsData:
            self.itemTree.insert(parent="",index=END,iid=sNO,text="parent",values=(sNO,item[0],item[1],item[2],item[3]))
            sNO+=1

class analysisLayout:
    def __init__(self,main):
        self.master=Frame(main)
        self.master.grid(row=0,column=0,sticky=NSEW)

if __name__ == "__main__":
    base=Tk()
    base.state("zoomed")
    mainLayout(base)
    base.mainloop()