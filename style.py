from tkinter import ttk
from tkinter.constants import BROWSE
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