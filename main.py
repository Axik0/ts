from tkinter import *
from PIL import Image, ImageTk

# icon import&resize (non-crappy thanks to pillow fork)
icon = Image.open("images/monkey.png")
icon = icon.resize((20, 20), Image.Resampling.LANCZOS)

# Global color palette
main_color = '#f0f3f5'
focus_color = '#fff0fb'
highlight_color = '#a2d1f2'

# GUI preliminaries
window = Tk()
window.configure(background=main_color)
window.geometry("600x300")
window.minsize(400, 200)
window.maxsize(600, 300)
window.title(" Typing monke")
icon_tk = ImageTk.PhotoImage(icon)
window.iconphoto(False, icon_tk)

window.mainloop()
