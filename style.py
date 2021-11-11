from tkinter import ttk
from tkinter import *
from PIL import Image,ImageTk

class stylesheet:

    def __init__(self):
        self.style=ttk.Style()
        self.styles()
        self.trickStyles()
        self.getTreeview()

    def styles(self):
        self.style.configure("C.TLabel",font=("impact",18,""))
        self.style.configure("pay.TMenubutton",font=("",18,""))

    def trickStyles(self):

        self.billingLabel={
            "font":("impact",18,""),

        }
        self.billingEntry={
            "font":("",18,""),
            "highlightcolor":"blue",
            "highlightthickness":1,
        }

        self.customerEntry={
            "font":("lucida fax",14,""),
            "highlightcolor":"lightgreen",
            "highlightthickness":1,
        }

        self.customerOption={
            "font":("lucida fax",14,""),
        }

        self.billingListLabel={
            "font":("",22,"")
        }


    def getTreeview(self):
        self.style.configure("bill.Treeview",
                            background="silver",
                            fieldbackground="red",
                            selectmode=BROWSE,
                            font=("",14),
                            )
        self.style.map("bill.Treeview",
                        background=[('selected','red')],
                        )

        self.style.configure("bill.Treeview.Heading",
                                font=("arial rounded MT bold",16))


class kartButton(Button):
    def __init__(self,master,file=None,command=None,text=None):
        super().__init__(master=master,border=0,command=command,text=text)
        if file:
            self.buttons=dict()
            self.ButtonResize(file)
            self.ButtBindings()

    def ButtonResize(self,fileName):
        
        buttonsType=["normal","hover","active"]
        for butTyp in buttonsType:
            resized=(Image.open("resource/ui/"+fileName+"_"+butTyp+".png")).resize((120,50),Image.ANTIALIAS)
            self.buttons[butTyp]=(ImageTk.PhotoImage(resized))
        self.config(image=self.buttons["normal"])
        
    def hover(self,event):
        event.widget.config(image=self.buttons["hover"])
    def hoverLeave(self,event):
        event.widget.config(image=self.buttons["normal"])
    def active(self,event):
        event.widget.config(image=self.buttons["active"])
    
    def ButtBindings(self):
        events=["<Enter>","<Leave>","<Button-1>","<ButtonRelease-1>"]
        eventsFunc=[self.hover,self.hoverLeave,self.active,self.hover]
        for x in range(0,len(events)):
            self.bind(events[x],eventsFunc[x])

