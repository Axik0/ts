from tkinter import *
from PIL import Image, ImageTk
import string
import time

# prepare character lists for future key bindings
LETTERS = list(string.ascii_lowercase)+list(string.ascii_uppercase)
DIGITS = list(string.digits)
# wow, this list automation takes even care of the problematic cases (includes both "'" and '"')
MARKS = list(string.punctuation)
EXTRAS = ['<space>']

EXAMPLE = 'Pineapple Apple Pen'
CHARSET = LETTERS+EXTRAS
TOP_CPS = 10

# image import&resize (non-crappy thanks to this pillow fork)
icon = Image.open("images/monkey.png")
icon = icon.resize((20, 20), Image.Resampling.LANCZOS)
rfr = Image.open("images/refresh.png")
rfr = rfr.resize((35, 35), Image.Resampling.LANCZOS)
tp = Image.open("images/click.png")
tp = tp.resize((35, 35), Image.Resampling.LANCZOS)

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
window.geometry("500x200")
window.minsize(520, 200)
window.maxsize(600, 300)
window.title(" Typing monke")
icon_tk = ImageTk.PhotoImage(icon)
window.iconphoto(False, icon_tk)


def binder(command, lst=CHARSET, mode=True):
    """takes key names from the list and binds/unbinds to/from a single callback"""
    for key in lst:
        text_field.bind(key, command) if mode else text_field.unbind(key)
# k_binder(test, ['a','w'], EXTRAS)


def text_handler(text: str):
    """processes and displays progress of user's typing in a text_field"""
    # insert the given text into the text field
    text_field.insert("1.0", text)
    # set a cursor (=insert mark) to starting position
    text_field.mark_set("insert", "1.0")
    # what if we don't allow typing but move (hidden) cursor and just color the current progress?
    text_field['state'] = 'disabled'

    # drop tempo variables to defaults
    window.scv.set(0)
    c_time, c_counter = 0, 0

    # prepare a variable to check for success and count errors
    curr_succ = BooleanVar()
    curr_succ.set(False)
    curr_error = IntVar()
    curr_error.set(0)

    # get ready to catch (and compare on the fly) inputs from a keyboard
    def check(key_pressed):
        """compares an event (some symbol has just been typed) with a next symbol (on the right) of the text line"""
        if key_pressed.char.lower() == text_field.get("insert", "insert+1c").lower():
            curr_succ.set(True)
        else:
            print(key_pressed.char)
            curr_error.set(curr_error.get()+1)
    binder(check, CHARSET)
    retry_butt['image'] = tp_tk
    for _ in text:
        tic = time.perf_counter()
        # stop, wait until curr_succ variable changes (False->True) i.e. until we will have got a correct key
        window.wait_variable(curr_succ)
        toc = time.perf_counter()
        curr_succ.set(False)
        # color everything up to and including current character to mark as processed (aka INActive)
        text_field.tag_add("prev", "1.0", "insert+1c")
        text_field.tag_config("prev", foreground=text_color_ina)
        # move cursor to the next character
        text_field.mark_set("insert", "insert+1c")
        # as our implementation starts automatically, let's drop very first cycle to be fair enough
        if c_counter != 0:
            c_time += toc - tic
        c_counter += 1
    # prevent user from typing any further, 2 lines could be deleted with a SAME gain but this way is more stable
    binder(check, mode=False)
    # after all, get rid of old tag and change the text color back to normal
    text_field.tag_delete("prev")
    text_field['fg'] = text_color_a
    retry_butt['image'] = rfr_tk
    # tempo calculations (with errors as )
    average_cps = (len(text) - 1 + curr_error.get())/c_time
    relative_cps = 100*average_cps/TOP_CPS
    window.scv.set(round(relative_cps))

head_label = Label(window, text="Start typing the line below:", font=main_font)
head_label.grid(row=0, column=0, columnspan=2, pady=5)

text_field = Text(window, bg=focus_color, fg=text_color_a, height=3, width=40, font=main_font, relief='sunken')
text_field.focus_set()
text_field.grid(row=1, column=0, columnspan=2, padx=18)

window.scv = IntVar()
w2 = Scale(window, from_=0, to=100, tickinterval=25, orient=HORIZONTAL, length=400, state=DISABLED, showvalue=False,
           font=main_font, label='SPEED', variable=window.scv, troughcolor=focus_color)
w2.grid(row=2, column=0, sticky=N+S+W+E, padx=15)

rfr_tk = ImageTk.PhotoImage(rfr)
tp_tk = ImageTk.PhotoImage(tp)
retry_butt = Button(text='Retry', image=rfr_tk, command=lambda: text_handler(EXAMPLE))
retry_butt.grid(row=2, column=1, sticky=N+S+W, ipadx=5, pady=10)

if __name__ == "__main__":
    text_handler(EXAMPLE)

window.mainloop()

# TODO toggle case sensitivity via button/slider