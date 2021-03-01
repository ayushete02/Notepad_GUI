import os
import platform
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from types import prepare_class
import PyPDF2

import win32gui
import win32con

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide, win32con.SW_HIDE)


root = Tk()
root.title("Untitled - Notepad")

Icon = PhotoImage(file='Logo/1.png')
root.iconphoto(False, Icon) 

root.geometry("1000x500")


def New():
    file = None
    root.title("Untitled - Notepad")
    Text_Editor.delete(1.0, END)

def New_Window():
    file = None
    os.startfile("Xfile.py")


def Open():
    global file
    global Current_path
    file = askopenfilename(defaultextension=".txt", filetypes=[(
        "All Files", "*.*"), ("Text Documents", "*.txt"), ("Python Document", "*.py"),("C Document", "*.c"),("PDF document","*.pdf")])
    Current_path = os.path.abspath(file)
    
 
    if file == "":
        file = None
    else:
        try:
            if os.path.basename(file).endswith(".pdf"):
                OpenPdf = PyPDF2.PdfFileReader(file)
                for i in range(OpenPdf.getNumPages()):
                    TextInPdf = OpenPdf.getPage(i).extractText()
                    Text_Editor.insert(1.0,TextInPdf)

                root.title(f"*{os.path.basename(file)} - Notepad")
                

            else:
                Text_Editor.delete(1.0, END)
                f = open(file)
                Text_Editor.insert(1.0, f.read())
                f.close()
                root.title(f"*{os.path.basename(file)} - Notepad")
        except:
            pass
            
    #print(file)


def Save():

    global file
    global Current_path
    try:
        #print(os.path.basename(file))
        #print(Current_path)
        root.title(f"{os.path.basename(file)} - Notepad")
        f = open(Current_path, "w")
        f.write(Text_Editor.get(1.0, END))
        f.close()
    except:
        Save_as()


def Save_as():
    global file
    if file == None:
        file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),("Python Document", "*.py"),("C Document", "*.c"),("PDF document","*.pdf")])
        if file == "":
            file = None
        else:
            f = open(file, "w")
            f.write((Text_Editor.get(1.0, END)))
            f.close()
            root.title(f"{os.path.basename(file)} - Notepad")
    else:
        #print(os.path.basename(file))
        #print(Current_path)
        f = open(Current_path, "w")
        f.write(Text_Editor.get(1.0, END))
        f.close()
        root.title(f"{os.path.basename(file)} - Notepad")


def printer():
    global file
    try:
        os.startfile(file, "print")
    except:
        Save_as()
        os.startfile(file, "print")



def cut():
    Text_Editor.event_generate(("<<Cut>>"))


def copy():
    Text_Editor.event_generate(("<<Copy>>"))


def paste():
    Text_Editor.event_generate(("<<Paste>>"))


def about():
    showinfo("About Notepad", "Notepad by Ayush Shete")


# Menu Bar
menubar = Menu(root)
m1 = Menu(menubar, tearoff=0)
m1.add_command(label="New", accelerator="Ctrl+N", command=New)
m1.add_command(label="New Window", accelerator="Ctrl+T", command=New_Window)
m1.add_command(label="Open...", accelerator="Ctrl+O", command=Open)
m1.add_command(label="Save", accelerator="Ctrl+S", command=Save)
m1.add_command(label="Save as...", accelerator="Ctrl+S", command=Save_as)
m1.add_separator()
m1.add_command(label="print", command=printer, accelerator="Ctrl+P")
m1.add_separator()
m1.add_command(label="Exit", command=quit, accelerator="Ctrl+E")
menubar.add_cascade(label="File", menu=m1)
root.config(menu=menubar)

m2 = Menu(menubar, tearoff=0)
m2.add_command(label="Undo", accelerator="Ctrl+Z")
m2.add_command(label="Redo", accelerator="Ctrl+Y")
m2.add_separator()
m2.add_command(label="Copy", accelerator="Ctrl+C", command=copy)
m2.add_command(label="Cut", accelerator="Ctrl+X", command=cut)
m2.add_command(label="paste", accelerator="Ctrl+V", command=paste)
m2.add_command(label="Delete")
m2.add_separator()
m2.add_command(label="Select all", accelerator="Ctrl+A")
menubar.add_cascade(label="Edit", menu=m2)
root.config(menu=menubar)

m3 = Menu(menubar, tearoff=0)
m3.add_command(label="Font")
m3.add_command(label="Size")
menubar.add_cascade(label="Format", menu=m3)
root.config(menu=menubar)

m4 = Menu(menubar, tearoff=0)
m4.add_command(label="Zoom")
m4.add_command(label="Find", accelerator="Ctrl+F")
menubar.add_cascade(label="View", menu=m4)
root.config(menu=menubar)

m5 = Menu(menubar, tearoff=0)
m5.add_command(label="View help", accelerator="Ctrl+H")
m5.add_command(label="Send feedback", accelerator="Ctrl+L")
m5.add_separator()
m5.add_command(label="About Notepad", command=about, accelerator="Ctrl+B")
menubar.add_cascade(label="Help", menu=m5)
root.config(menu=menubar)


# Working Space
Text_Editor = Text(root,font = 15)
file = None
Current_path = None
Text_Editor.pack(fill=BOTH, expand=True)


# Scroll bar

Scroll = Scrollbar(Text_Editor)
Scroll.pack(side=RIGHT, fill=Y)
Scroll.config(command=Text_Editor.yview)
Text_Editor.config(yscrollcommand=Scroll.set)

# Footer
Footer = Frame(root)
Footer.pack(fill=X, side=BOTTOM)
UTF = Label(Footer, text="UTF = 8                 ", relief='sunken', border=1, padx=10)
UTF.pack(side=RIGHT)

Device = Label(
    Footer, text=f'''{platform.system()}({platform.release()})    ''',relief='sunken', border=1, padx=10)
Device.pack(side=RIGHT)


Position = Text_Editor.index("current")
ln  = Position.split('.')[0]
Col =Position.split('.')[1]
Cursor = Label(Footer,text=f"ln {ln} ; col {Col}",relief='sunken', border=1, padx=10)
Cursor.pack(side=RIGHT)
def set_value(event):
    global Cursor
    Cursor.pack_forget()
    Position = Text_Editor.index("current")
    ln  = Position.split('.')[0]
    Col =Position.split('.')[1]
    Cursor = Label(Footer,text=f"ln {ln} ; col {Col}",relief='sunken', border=1, padx=10)
    Cursor.pack(side=RIGHT)


Text_Editor.bind('<KeyRelease>',set_value)

# keys
def Title(event):
    global file
    if file !=None:
        #print(os.path.basename(file))
        root.title(f"*{os.path.basename(file)} - Notepad")
    else:
        #print("Untitled")
        root.title(f"*Untitled - Notepad")

Text_Editor.bind("<Button-1>",Title)


def New_event(event):
    New()


Text_Editor.bind("<Control-n>", New_event)


def New_w_event(event):
    New_Window()


Text_Editor.bind("<Control-t>", New_w_event)


def Open_event(event):
    Open()


Text_Editor.bind("<Control-o>", Open_event)


def Save_event(event):
    Save()


Text_Editor.bind("<Control-s>", Save_event)


def Save_as_event(event):
    Save_as()


Text_Editor.bind("<Control-s>", Save_as_event)


def printer_event(event):
    printer()


Text_Editor.bind("<Control-p>", printer_event)


def quit_event(event):
    quit()


Text_Editor.bind("<Control-e>", quit_event)


def about_event(event):
    about()


Text_Editor.bind("<Control-b>", about_event)


root.mainloop()










