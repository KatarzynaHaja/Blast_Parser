from tkinter import Tk, BOTH
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import PIL.Image
from PIL import ImageTk
import tkinter.messagebox
from parser_blast import *
import os
from generate_report import Generate_report_pdf
from summary import Summary

class Main_frame(Frame):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.center_window()


    def init_ui(self):
        self.loaded=False
        self.master.title("Blast Parser")
        self.pack(fill=BOTH, expand=True)

        photo =PIL.Image.open(os.path.join("static",'dna.jpg'))
        ph = ImageTk.PhotoImage(photo)

        self.main_quotes= ttk.Label(self.master,text="Blast parser, load data and enjoy",foreground="white",font="Georgia",compound="bottom",image=ph)
        self.main_quotes.ph = ph
        self.main_quotes.pack()

        self.text_area = Text(self.master,height=9, width=25)
        self.text_area.pack()
        self.text_area.place(x=400, y=100)
        self.text_area.config(font="Georgia")

        self.load_from_file = ttk.Button( self.master,text="Load from file",command= self.load)
        self.load_from_file.place(x=50, y=200)

        self.submit = ttk.Button(self.master, text="Submit", command=self.submit_message)
        self.submit.place(x=430, y=280)

        self.clear= ttk.Button(self.master, text="Clear", command=self.clear)
        self.clear.place(x=550, y=280)

        self.export_to_excel = ttk.Button(self.master, text="Export to Excel",command=self.export_to_excel)
        self.export_to_excel.place(x=150, y=200)

        self.generate_charts = ttk.Button(self.master, text="Generate pdf report", command=self.generate_report_pdf)
        self.generate_charts.place(x=250, y=200)


    def submit_message(self):
        input =  self.text_area.get("1.0",'end-1c')
        print(input)
        if len(input)!=0:
            with open(os.path.join("files","blaaa.xml"),'w') as file:
                file.write(input)
            self.p = ParserBlast(os.path.join("files","blaaa.xml"))
            self.loaded= True

        else:
            tkinter.messagebox.showinfo("Blast", "Text box is empty, try again!")

    def clear(self):
        self.text_area.delete('1.0', END)

    def export_to_excel(self):
        if self.loaded == True:
            s = Summary(self.p)
            t = s.export_to_excel()
            print(t)
            if t == "":
                tkinter.messagebox.showinfo("Blast", "Your didn't choose file")
            else:
                tkinter.messagebox.showinfo("Blast", "Your data has been saved in excel")
        else:
            tkinter.messagebox.showinfo("Blast", "Data has not loaded, try again!")

    def generate_report_pdf(self):
        if self.loaded == True:
            filename = filedialog.asksaveasfilename(filetypes=(("Pdf files", "*.pdf"),
                                                               ("All files", "*.*")))
            print(filename)

            if filename == '':
                tkinter.messagebox.showinfo("Blast", "Your didn't choose file")
            else:
                if re.search("pdf", filename) is None:
                    filename = filename + ".pdf"
                Generate_report_pdf(self.p,filename)
                tkinter.messagebox.showinfo("Blast", "Your data has been saved in pdf")

        else:
            tkinter.messagebox.showinfo("Blast", "Data has not loaded, try again!")

    def center_window(self):
        w = 700
        h = 400

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def load(self):
        self.file_name = filedialog.askopenfilename(filetype=(("xml", ".xml"), ("all files", "*.*")))
        if len(self.file_name)!= 0:
            self.parse()
            self.loaded = True
            tkinter.messagebox.showinfo("Blast", "Loaded succesfuly")
        else:
            tkinter.messagebox.showinfo("Blast", "You don't choose any file, try again!")

    def parse(self):
        self.p = ParserBlast(self.file_name)


def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = Main_frame()
    app.mainloop()

main()

