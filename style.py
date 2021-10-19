from tkinter import ttk
class stylesheet:
    def __init__(self):
        self.billingStyle=ttk.Style()
        self.styles()
        self.trickStyles()

    def styles(self):
        self.billingStyle.configure("C.TLabel",font=("impact",18,""))
        self.billingStyle.configure("pay.TMenubutton",font=("",18,""))

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