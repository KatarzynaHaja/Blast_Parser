from tkinter import Tk, BOTH
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import PIL.Image
from PIL import ImageTk
import tkinter.messagebox

class Main_frame(Frame):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.center_window()


    def init_ui(self):
        self.master.title("Blast Parser")
        self.pack(fill=BOTH, expand=True)

        photo =PIL.Image.open('dna.jpg')
        ph = ImageTk.PhotoImage(photo)

        self.main_quotes= ttk.Label(self.master,text="Blast parser, load data and enjoy",foreground="white",font="Georgia",compound="bottom",image=ph)
        self.main_quotes.ph = ph
        self.main_quotes.pack()

        self.text_area = Text(self.master,height=9, width=25)
        self.text_area.pack()
        self.text_area.place(x=400, y=100)
        self.text_area.insert(INSERT, "Paste output of blast")
        self.text_area.config(font="Georgia")

        load_from_file = ttk.Button( self.master,text="Load from file",command= self.load)
        load_from_file.place(x=100, y=200)

        self.submit = ttk.Button(self.master, text="Submit", command=self.submit_message)
        self.submit.place(x=480, y=280)

    def submit_message(self):
        tkinter.messagebox.showinfo("Blast", "Your data has been loaded")
        input =  self.text_area.get("1.0",'end-1c')
        print(input)


    def center_window(self):
        w = 700
        h = 400

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def load(self):
        file_name = filedialog.askopenfilename(filetype=(("txt", ".txt"), ("all files", "*.*")))
        print(file_name)
        return file_name


def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = Main_frame()
    app.mainloop()

main()

