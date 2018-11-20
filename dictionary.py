import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox as m_box
from tkinter import Menu
import json
from difflib import get_close_matches
import cv2
import PIL.Image
import PIL.ImageTk

data = json.load(open("data.json"))


class CreateWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Dictionary")

        # Creating a Menu Bar

        self.menu_bar = Menu(master)
        self.master.config(menu=self.menu_bar)

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self._quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.image_path = "image.jpg"
        self.cv_img = cv2.cvtColor(cv2.imread(self.image_path), cv2.COLOR_BGR2RGB)

        self.canvas = tk.Canvas(master, width=self.cv_img.shape[1], height=self.cv_img.shape[0])
        self.canvas.pack()

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))

        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Creating Label frames

        self.labelframe1 = ttk.LabelFrame(self.master)
        self.labelframe1.pack(fill=tk.BOTH, expand=1)

        self.labelframe2 = ttk.LabelFrame(self.master)
        self.labelframe2.pack(fill=tk.BOTH, expand=1)

        # Tk Variable
        self.entered_word = tk.StringVar()

        # Customized font
        self.customized_font = font.Font(family='Helvetica', size=14,
                                         weight="bold")
        self.style = ttk.Style()
        self.style.configure("buttons.TButton", foreground="green", font=('Helvetica', 12))

        # Creating Labels
        self.label = tk.Label(self.labelframe1, text="Enter a word : ", font=self.customized_font)
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Creating entry Fields
        self.entry_field = ttk.Entry(self.labelframe1, textvariable=self.entered_word, width=30)
        self.entry_field.grid(row=0, column=1, padx=10, pady=10, sticky="W")

        # Creating buttons
        self.search_btn = ttk.Button(self.labelframe2, text="Search", command=self.get_results,
                                     width=15, style="buttons.TButton")
        self.search_btn.pack(anchor=tk.CENTER, pady=10)
        self.entry_field.focus()

    def get_results(self):
        w = self.entered_word.get().lower().strip(" ")
        if len(w) == 0:
            m_box.showwarning('...', 'Enter a word')
        else:
            found = ''
            meanings = ''
            flag = 0
            if w in data:
                found = "YES"
                meanings = data[w]

            elif len(get_close_matches(w, data.keys())) > 0:

                ans = m_box.askyesno("...", f"Did you mean "
                                            f"{get_close_matches(w, data.keys())[0]} instead ?")

                if ans is True:
                    found = "YES"
                    meanings = data[get_close_matches(w, data.keys())[0]]
                    flag = 1
                elif ans is False:
                    m_box.showerror("...", "The word doesn't exist. Please double check it.")

            else:
                m_box.showerror('...', 'Not Found!!!')

            if found == "YES":
                if flag == 1:
                    w = get_close_matches(w, data.keys())[0]

                output = ''
                for item in meanings:
                    output += '\n\n' + item
                m_box.showinfo("...", f"{w.upper()} means -> {output}")

    def _quit(self):
        self.master.quit()
        self.master.destroy()
        exit()

    def about(self):
        m_box.showinfo('About', 'Created by : Anamitra Mukherjee')


def main():
    win = tk.Tk()
    CreateWindow(win)
    win.mainloop()


if __name__ == '__main__':
    main()
