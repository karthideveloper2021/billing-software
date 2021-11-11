from tkinter import *  
from tkinter import ttk,messagebox
from style import stylesheet,kartButton
import database
import time
from configparser import ConfigParser
import threading
import winsound
from PIL import Image,ImageTk

class mainLayout:
    def __init__(self,main):
        self.master=main
        self.menu()
        self.header()
        self.content() 
        self.footer()               
        
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
        self.data()

    def footer(self):
        self.foot=footer(self.master)

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
        self.currentDate()

    def currentDate(self):
        self.dateLabel=Label(self.headerFrame,text=time.strftime("%d/%m/%Y"))
        self.dateLabel.pack(side=RIGHT,padx=10,pady=5)
        self.dateLabel.config(
            background="black",
            foreground="white",
            font=("",18,"")
        )       

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

class footer:
    def __init__(self,main):
        self.master=main
        self.statusBar()
    
    def statusBar(self):
        self.status=Frame(self.master)
        self.status.pack(side=BOTTOM,fill=X)

class getDataLayout:
    def __init__(self,main):
        self.master=Frame(main)
        self.master.grid(row=0,column=0,sticky=NSEW)
        stylesheet().getTreeview()
        self.initialize()
        self.billingInput()
        self.billingList()
        self.keyBindings()

    
    def billingInput(self):
        
        self.getFrame=Frame(self.master,bg="red")
        self.getFrame.pack(side=LEFT,anchor=N,padx=25)

        self.initializeValidate()
        self.addReset=Frame(self.getFrame)

        self.inputFont=("",18,"")
        self.LabelFont=("impact",18,"")
        self.itemLabel=Label(self.getFrame,text="ITEM NO",**stylesheet().billingLabel)
        self.itemNO=Entry(self.getFrame,**stylesheet().billingEntry,validate="key",validatecommand=(self.entryIntReg,"%P"))
        self.itemNameLabel=Label(self.getFrame,text="ITEM NAME",**stylesheet().billingLabel)
        self.itemName=Entry(self.getFrame,**stylesheet().billingEntry)
        self.quantityLabel=Label(self.getFrame,text="QUANTITY",**stylesheet().billingLabel)
        self.quantity=Entry(self.getFrame,**stylesheet().billingEntry,validate="key",validatecommand=(self.entryFloatReg,"%P"))
        self.add=Button(self.addReset,text="ADD",font=self.LabelFont,width=10,command=self.addCart)
        self.reset=Button(self.addReset,text="RESET",font=self.LabelFont,width=10,command=self.deleteInputs)

        self.itemLabel.pack(pady=10)
        self.itemNO.pack(pady=10,padx=20)
        self.itemNameLabel.pack(pady=10,padx=20)
        self.itemName.pack(pady=10,padx=20)
        self.quantityLabel.pack(pady=10,padx=20)
        self.quantity.pack(pady=10,padx=20)
        self.add.pack(side=LEFT,padx=10)
        self.reset.pack(side=LEFT,padx=10)
        self.addReset.pack(pady=5)
        
        self.itemNO.focus_set()

        self.customerDetails()

        self.print=Button(self.getFrame,text="PRINT",font=self.LabelFont,command=self.billingUpload)
        self.print.pack(pady=10)
    
        print(self.itemNO.winfo_class())

        self.searchFrame=Frame(self.getFrame)
        self.search=Listbox(self.searchFrame,font=self.itemName.cget('font'),height=4,selectmode=BROWSE,selectbackground="red",activestyle="dotbox")
        self.search.pack(side=LEFT)
        self.searchScroll=Scrollbar(self.searchFrame,orient=VERTICAL,command=self.search.yview)
        self.searchScroll.pack(side=RIGHT,fill=Y)
        self.search.config(yscrollcommand=self.searchScroll.set)

    def customerDetails(self):
        
        self.comboFont=("lucida fax",14,"")

        self.customerDetailsFrame=Frame(self.getFrame)
        self.customerDetailsFrame.pack(pady=50)

        self.cusNameLabel=Label(self.customerDetailsFrame,text="CUSTOMER NAME",**stylesheet().billingLabel)
        self.cusName=Entry(self.customerDetailsFrame,**stylesheet().customerEntry)
        self.cuspnLabel=Label(self.customerDetailsFrame,text="CUSTOMER PHONE.NO",**stylesheet().billingLabel)
        self.cuspn=Entry(self.customerDetailsFrame,**stylesheet().customerEntry)
        self.payModeLabel=Label(self.customerDetailsFrame,text="PAYMENT",**stylesheet().billingLabel)
        
        self.paySelect=StringVar()
        self.payList=["CASH","CARD","UPI"]
        self.paySelect.set(self.payList[0])
        self.payMode=OptionMenu(self.customerDetailsFrame,self.paySelect,*self.payList)
        self.payMode.config(**stylesheet().customerOption)
        self.payModeOption=self.customerDetailsFrame.nametowidget(self.payMode.menuname)
        self.payModeOption.config(**stylesheet().customerOption)
    
        self.cusNameLabel.grid(row=0,column=0,pady=5,padx=10,sticky=W)
        self.cusName.grid(row=0,column=1,pady=5,padx=10)
        self.cuspnLabel.grid(row=1,column=0,pady=5,padx=10)
        self.cuspn.grid(row=1,column=1,pady=5,padx=10)
        self.payModeLabel.grid(row=2,column=0,pady=5,padx=10)
        self.payMode.grid(row=2,column=1,pady=5,padx=10,sticky=W)


    def billingList(self):
        
        self.billingViewFrame=Frame(self.master,bg="green")
        self.billingViewFrame.pack(side=LEFT,padx=5,fill=BOTH,expand=1)
      
        self.billingInfo()
        self.billingListFrame=Frame(self.billingViewFrame)
        self.billingListFrame.pack(pady=5,fill=BOTH,expand=1)

        self.itemsList=ttk.Treeview(self.billingListFrame,style="bill.Treeview")
        self.itemsList.pack(side=LEFT,pady=5,fill=BOTH,expand=1)
      

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

        self.remList=ttk.Treeview(self.billingListFrame)
        self.remList.pack(side=LEFT,fill=Y,pady=5,padx=0)
        self.remImage=PhotoImage(file="resource/ui/remove.png")
        self.remList.column("#0",width=50,stretch=OFF,anchor=W)
        
        self.itemsListScroll=Scrollbar(self.billingListFrame)
        self.itemsListScroll.pack(side=LEFT,fill=Y)
        self.itemsList.config(yscrollcommand=self.itemsListScroll.set)
        self.remList.config(yscrollcommand=self.itemsListScroll.set)
        #self.itemsList.configure("removeItem",image=remImage)

        def makeSelection(event):
        
            row=event.widget.focus()
            #print(event.widget.item(row,'values'))
            print(self.itemsList.item(row)['values'])
        def removeItem(event):
            pass
            # for line in self.itemsList.get_children():
            #     value=self.itemsList.item(line)['values']
            #     if value[1]==itemNO:
            #         self.itemsList.delete(line)
            #         for widget in self.remList.winfo_children():
            #             if widget.cget('text')==itemNO:
            #                 widget.destroy()
            #                 break
        

        self.itemsList.bind("<Button-1>",makeSelection)
        self.remList.bind("<Button-1>",removeItem)
        self.billingCheckout() 
        

    def billingInfo(self):
        self.billingNumNext()
        self.billingInfoFrame=Frame(self.billingViewFrame,bg="blue")
        self.billingInfoFrame.pack(side=TOP,fill=X)

        self.title=Label(self.billingInfoFrame,
                            text="BILLING",
                            font=("rockwell",20,"bold"))
        self.title.pack()

        self.billNoLabel=Label(self.billingInfoFrame,text="BILL NO",
                            font=("cambria",16,"bold"))
        self.billNoLabel.pack(side=LEFT,padx=10)

        self.billNo=Label(self.billingInfoFrame,text=self.billNum,
                            font=("cambria",14,""))
        self.billNo.pack(side=LEFT,padx=5)
        

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
        print(self.customerCount)   
        self.billNum="B"+date[:2]+date[3:5]+time.strftime("%y")+str(self.customerCount)
        print(self.billNum)

    def configWriting(self):
        with open("settings.ini","w") as settingsFile:
            self.parserControl.write(settingsFile)

    def billingCheckout(self):
        self.checkoutFrame=Frame(self.billingViewFrame,bg="brown")
        self.checkoutFrame.pack(side=RIGHT,anchor=S,padx=50,pady=10)

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
        self.prepareEverythingForNext()
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

        itemdetails=self.billingObj.getItemSpecific(self.itemNO.get())
        if self.add.cget('text')=="ADD":
            self.totalItems+=1 
            self.totalAmt=float(self.quantity.get())*itemdetails[2]
            self.itemsList.insert(parent="",index=END,
                        values=(self.totalItems,itemdetails[0],itemdetails[1],self.quantity.get(),itemdetails[2],self.totalAmt))
            self.remList.insert("",index=END,image=self.remImage)

        elif self.add.cget('text')=="UPDATE":
            self.totalAmt=float(self.quantity.get())*itemdetails[2]
            print(self.totalAmt)
            for line in self.itemsList.get_children():               
                value= self.itemsList.item(line)['values']
                if int(self.itemNO.get())==value[1]:
                    self.itemsList.item(line,values=(value[0],value[1],value[2],self.quantity.get(),value[4],self.totalAmt))
                    break
        self.updateTotalinfo()
        self.deleteInputs()
    
   
    def prepareEverythingForNext(self):
        self.itemsList.delete(*self.itemsList.get_children())
        self.remList.delete(*self.remList.get_children())
        self.deleteInputs()
        self.cusName.delete(0,END)
        self.paySelect.set(self.payList[0])
        self.updateTotalinfo()

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

   
    def keyBindings(self):
        
        self.notFound=Label(self.getFrame,text="Item not found")
        def itemNocheck(event):
            self.itemName.delete(0,END)
            self.quantity.delete(0,END)
            if self.itemNO.get()=="":
                self.itemName.focus_set()
            else:
                #if self.itemNO.get() in self.CartItemsDic.keys():
                itemsData=self.billingObj.getItemSpecific(int(self.itemNO.get()))
                if itemsData is not None:
                    for line in self.itemsList.get_children():               
                        value= self.itemsList.item(line)['values']
                        if int(self.itemNO.get())==value[1]:
                            self.add.config(text="UPDATE")
                            break
                                          
                    self.itemName.insert(0,itemsData[1])
                    self.quantity.focus_set()
                else:
                    self.notFound.place(x=self.itemNO.winfo_x(),y=self.itemNO.winfo_y()-20)

        def hideItemNOStuff(event):
            self.notFound.place_forget()
            self.add.config(text="ADD")

        def addingProcess(event):
            self.addCart()
            self.add.config(text="ADD")
        
        def searchListPlace():
        
            self.searchFrame.place(x=self.itemName.winfo_x(),y=self.itemName.winfo_y()+2*self.itemName.cget('width'))
            itemsData=self.billingObj.getItemProcessItemNames()
            print(itemsData)
            for items in itemsData:
                if self.itemName.get().lower() in items[0].lower():
                    self.search.insert(END,items[0])

        def searchProcess(event):
            self.search.delete(0,END)
            if self.itemName.get()=="" or event.keysym=="Escape":
                self.searchFrame.place_forget()
                self.itemName.focus_set()
            else:
                searchListPlace()
        
        def updateSearch(event):
            print(event.widget.curselection()[0])
            itemData=self.billingObj.getItemName(event.widget.get(event.widget.curselection()[0]))
            print(itemData)
            self.deleteInputs()
            self.itemNO.insert(0,itemData[0])
            self.itemName.insert(0,itemData[1])
            self.searchFrame.place_forget()
            self.quantity.focus_set()
        
        def listItemSelection(event):
            key=event.keysym
            if key=="Up":
                if event.widget.curselection()[0]==0:
                    self.itemName.focus_set()            
            elif key=="Down":
                self.search.focus_set()
                self.search.activate(0)
                self.search.selection_set(0)

        def listCursorSelection(event):
            #print(event.widget.curselection()[0])
            self.search.selection_clear(0,END)
            self.search.focus_set()
            for i in range(0,event.widget.size()):
                element=event.widget.bbox(i)
                print(element)
                if element:
                    if element[1]<=event.y and (element[1]+element[3])>=event.y:
                        self.search.activate(i)
                        self.search.selection_set(i)
                        break
                

        
        self.itemNO.bind("<Tab>",itemNocheck)
        self.itemNO.bind("<Return>",itemNocheck)
        self.itemNO.bind("<KeyPress>",hideItemNOStuff)
        self.quantity.bind("<Return>",addingProcess)

        self.itemName.bind("<KeyRelease>",searchProcess)
        self.itemName.bind("<Down>",listItemSelection)
        #self.search.bind("<<ListboxSelect>>",updateSearch)
        self.search.bind("<Return>",updateSearch)
        self.search.bind("<Button-1>",updateSearch)
        self.search.bind("<Motion>",listCursorSelection)
        self.search.bind("<Up>",listItemSelection)
        self.search.bind("<Escape>",searchProcess)
        self.search.bind("<MouseWheel>",listCursorSelection)
        
        #self.search.see(10)
    
    def initializeValidate(self):
        def intCallBack(value):
            if value.isdigit() or value=="":
                return True
            else:
                return False
        def floatCallBack(value):
            if value.isdigit() or value=="":
                return True
            else:
                try:
                    float(value)
                    return True
                except:
                    return False
        self.entryIntReg=self.getFrame.register(intCallBack)
        self.entryFloatReg=self.getFrame.register(floatCallBack)
        
class insertDataLayout:
    def __init__(self,main):

        self.master=Frame(main)
        #self.master.place(x=0,y=0)
        self.master.grid(row=0,column=0,sticky=NSEW)   

        self.style=ttk.Style(self.master)    
        #stylesheet().getTreeview()
        self.initializeDb()
        #self.inputBox()
        self.searchFilter()
        self.listView()
        self.tools()
        self.keybindings()
        
    def initializeDb(self):
        self.conDat=database.connectData()
    
    def searchFilter(self):
        self.searFil=LabelFrame(self.master,text="Search & Filter")
        self.searFil.pack(side=TOP,padx=50,pady=5,fill=X)

        self.rateFromLabel=Label(self.searFil,text="Rate: From")
        self.rateToLabel=Label(self.searFil,text="To")

        self.search=Entry(self.searFil,width=50,**stylesheet().billingEntry)
        self.rateFrom=Entry(self.searFil,width=10,**stylesheet().billingEntry)
        self.rateTo=Entry(self.searFil,**stylesheet().billingEntry)

        self.search.pack(side=LEFT,padx=50,pady=10)
        self.rateFromLabel.pack(side=LEFT,padx=20,pady=10)
        self.rateFrom.pack(side=LEFT,padx=10,pady=10)
        self.rateToLabel.pack(side=LEFT,padx=10,pady=10)
        self.rateTo.pack(side=LEFT,padx=20,pady=10)


    def inputBox(self):
        self.putFrame=Toplevel(self.master)
        self.putFrame.transient(self.master)
        threading.Thread(target=lambda:winsound.PlaySound("*", winsound.SND_ALIAS)).start()
        
        #self.putFrame.pack(side=LEFT,padx=50,pady=100,anchor=N)
        print(int(self.master.winfo_rootx()/2))
        #self.putFrame.place(x=int(self.master.winfo_screenwidth()/2),y=int(self.master.winfo_rooty()/2))

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

        self.listFrame=Frame(self.master,bg="yellow")
        self.listFrame.pack(side=LEFT,padx=50,fill=BOTH,expand=1)

        self.style.configure("db.Treeview",
                            font=("",13),
                                                       
                            )
        self.style.configure("db.Treeview.Heading",
                            font=("",15,"bold"),
                                                       
                            )

        self.itemTree=ttk.Treeview(self.listFrame,style="db.Treeview")
        self.itemTree.pack(side=LEFT,fill=BOTH,expand=1)
    
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
       

    def tools(self):
            self.toolFrame=Frame(self.listFrame)
            self.toolFrame.pack(side=LEFT,fill=Y)

            self.add=kartButton(master=self.toolFrame,command=self.inputBox,file="add_item_but")
            self.delet=kartButton(master=self.toolFrame,file="del_item_but")
            self.export=kartButton(master=self.toolFrame,text="EXPORT")

            self.add.pack(padx=10,pady=10)
            self.delet.pack(padx=10,pady=10)
            self.export.pack(padx=10,pady=10)

    def insertTreeDatabase(self):

        #self.itemTree.insert(parent="",index=END,iid=0,values=("1","2","3","4","5","6"))
        itemsData=self.conDat.getItemProcess()
        sNO=0
        for item in itemsData:
            sNO+=1
            self.itemTree.insert(parent="",index=END,iid=sNO,text="parent",values=(sNO,item[0],item[1],item[2],item[3]))
    

    def keybindings(self):
        def searching(event):
            self.itemTree.delete(*self.itemTree.get_children())
            itemData=self.conDat.getItemProcess()
            sNO=1
            if self.search.get()!="":
                for record in itemData:
                
                    if self.search.get().lower() in record[1].lower():
                        print("test",record[1].lower())
                        self.itemTree.insert("",END,values=(sNO,record[0],record[1],record[2],record[3]))
                        sNO+=1
                    elif self.search.get().isdigit():
                        if self.search.get() in str(record[0]):
                            self.itemTree.insert("",END,values=(sNO,record[0],record[1],record[2],record[3]))
                            sNO+=1
            else:
                self.insertTreeDatabase()
        self.search.bind("<KeyRelease>",searching)

class analysisLayout:
    def __init__(self,main):
        self.master=Frame(main)
        self.master.grid(row=0,column=0,sticky=NSEW)

if __name__ == "__main__":
    base=Tk()
    base.state("zoomed")
    mainLayout(base)
    base.mainloop()