from tkinter import *
from PIL import Image, ImageTk
import string

# prepare character lists for future key bindings
LETTERS = list(string.ascii_lowercase)
DIGITS = list(string.digits)
# wow, this list automation takes care of  problematic cases (includes both "'" and '"')
MARKS = list(string.punctuation)
EXTRAS = ['<space>', '<Return>']

EXAMPLE = 'Pineapple Apple Pen'
CHARSET = LETTERS+EXTRAS

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

# GUI preliminaries
window = Tk()
window.configure(background=main_color)
window.geometry("600x300")
window.minsize(400, 200)
window.maxsize(600, 300)
window.title(" Typing monke")
icon_tk = ImageTk.PhotoImage(icon)
window.iconphoto(False, icon_tk)


def binder(command, lst=CHARSET, mode=True):
    """takes key names from the list and binds/unbinds to/from a single callback"""
    for key in lst:
        text_field.bind(key, command) if mode else text_field.unbind(key)

# k_binder(test, ['a','w'], EXTRAS)



main_label = Label(window, text="something", font=main_font)
main_label.pack()

# butt = Button(text='test', width=15, height=3, command=callback)
# butt.pack()

text_field = Text(window, bg=focus_color, fg=text_color_a, height=100, width=100, font=main_font, relief='sunken')

text_field.pack()
text_field.focus_set()

# window.bind('d', check)

# print(text_field.index(INSERT))
# text_field.delete("insert-1c", "insert")
# print(text_field.get("1.0", "end-1c"))


def text_handler(text: str):
    # insert the given text into the text field
    text_field.insert("1.0", text)
    # set a cursor (=insert mark) to starting position
    text_field.mark_set("insert", "1.0")
    # what if we don't allow typing but move a cursor and color current progress?
    text_field['state'] = 'disabled'

    # prepare a variable to check for success
    curr_succ = BooleanVar()
    curr_succ.set(False)

    # get ready to catch (and compare on the fly) inputs from a keyboard
    def check(key_pressed):
        """compares an event (some symbol has just been typed) with a next symbol (on the right) of the text line"""
        if key_pressed.char == text_field.get("insert", "insert+1c").lower():
            curr_succ.set(True)
            print(key_pressed.char)
        # delete this character anyway;
        # text_field.delete("insert-1c", "insert")
    binder(check, CHARSET)
    for _ in text:
        # stop, wait until curr_succ variable changes (False->True) i.e. until we will have got a correct key
        window.wait_variable(curr_succ)
        curr_succ.set(False)
        # color everything up to and including current character to mark as processed (aka INActive)
        text_field.tag_add("prev", "1.0", "insert+1c")
        text_field.tag_config("prev", foreground=text_color_ina)
        # move cursor to the next character
        text_field.mark_set("insert", "insert+1c")
    # prevent user from typing any further, 2 lines could be deleted with a SAME gain but this way is more stable
    binder(check, mode=False)
    # after all, get rid of old tag and change the text color back to normal
    text_field.tag_delete("prev")
    text_field['fg'] = text_color_a
    # text_handler(text)


text_handler(EXAMPLE)

window.mainloop()

# TODO toggle case sensitivity via button/slider
# TODO measure the time required for 1 character analysis to subtract this value * text_length from overall results
# TODO some kind of scoreboard
# FIXME move interface into a separate file, mb run asynchronously?
