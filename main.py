from tkinter import *
from PIL import Image, ImageTk

# icon import&resize (non-crappy thanks to this pillow fork)
icon = Image.open("images/monkey.png")
icon = icon.resize((20, 20), Image.Resampling.LANCZOS)

# Global color palette
main_color = '#f0f3f5'
focus_color = '#fff0fb'
text_color_a = '#262626'
text_color_ina = '#848484'

# Global font
main_font = ("Helvetica", 16)

EXAMPLE = 'wwwwww3422341d'

# GUI preliminaries
window = Tk()
window.configure(background=main_color)
window.geometry("600x300")
window.minsize(400, 200)
window.maxsize(600, 300)
window.title(" Typing monke")
icon_tk = ImageTk.PhotoImage(icon)
window.iconphoto(False, icon_tk)

main_label = Label(window, text="something", font=main_font)
main_label.pack()

text_field = Text(window, bg=focus_color, fg=text_color_a, height=100, width=100, font=main_font, relief='sunken')
text_field.insert("1.0", EXAMPLE)
text_field.pack()
text_field.focus_set()
text_field.mark_set(INSERT, "insert-1c")
print(text_field.index(INSERT))
text_field.delete("insert-1c", INSERT)
print(text_field.get("1.0", "end-1c"))

# for all char in length_EXAMPLE
# set cursor / counter to 1,0
c_ind = 0
# wait for input
# get last character, compare with next
# if same then change text color, move cursor
# if True:
#     text_field.config(fg=text_color_ina)
#     c_ind += 1
# else delete this character



window.mainloop()

# TODO toggle case sensitivity via button/slider
# TODO measure the time required for 1 character analysis to subtract this value * text_length from overall results
# TODO some kind of scoreboard
# FIXME move interface into a separate file, mb run asynchronously?
