from tkinter import *
from PIL import Image, ImageTk
import string
import time

# prepare character lists for future key bindings
LETTERS_L = set(string.ascii_lowercase)
LETTERS_U = set(string.ascii_uppercase)
DIGITS = set(string.digits)
# wow, this list automation takes even care of the problematic cases (includes both "'" and '"')
MARKS = set(string.punctuation)-{"#"}
EXTRAS = ['<space>']

EXAMPLE = 'Pineapple, Apple Pen'
TOP_CPS = 10

charset = set.union(LETTERS_L, LETTERS_U, EXTRAS, MARKS-{"<"})
markset = set.union(MARKS-{"<"}, {" "})

em = False

# image import&resize (non-crappy now thanks to this pillow fork)
icon = Image.open("images/monkey.png")
icon = icon.resize((35, 35), Image.Resampling.LANCZOS)
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
window.geometry("520x225")
window.minsize(520, 225)
window.maxsize(600, 300)
window.title("Typing Monke")
icon_tk = ImageTk.PhotoImage(icon)
window.iconphoto(False, icon_tk)


def binder(command, lst=charset, mode=True):
    """takes key names from the list and binds/unbinds to/from a single callback"""
    for key in lst:
        text_field.bind(key, command) if mode else text_field.unbind(key)


def text_handler(text: str):
    """processes and displays progress of user's typing in a text_field"""
    # insert the given text into the text field
    text_field.insert("1.0", text)
    # set a cursor (=insert mark) to starting position
    text_field.mark_set("insert", "1.0")
    # what if we don't allow typing but move (hidden) cursor and just color the current progress?
    text_field['state'] = 'disabled'

    # get settings from checkbuttons
    settings = s1.get(), s2.get()

    # drop tempo variables to defaults
    window.scv.set(0)
    c_time, c_counter = 0, 0

    # after/before all, get rid of old tag and change the text color back to normal
    # luckily it works even if "prev" doesn't exist yet so I can leave it here
    text_field.tag_delete("prev")
    text_field['fg'] = text_color_a

    # prepare a variable to check for success and count errors
    curr_succ = BooleanVar()
    # has to change in order to skip possibly unfinished game
    curr_succ.set(True)
    curr_succ.set(False)
    curr_error = IntVar()
    curr_error.set(0)

    # get ready to catch (and compare on the fly) inputs from a keyboard
    def check(key_pressed):
        """compares an event (some symbol has just been typed) with a next symbol (on the right) of the text line"""
        if key_pressed.char.lower() == next_char.lower() or key_pressed.char.upper() == next_char.upper():
            # if our characters differ only by their cases, compare precisely or skip if the setting allows
            if key_pressed.char == next_char or not settings[1]:
                curr_succ.set(True)
        elif settings[0] and prev_char in markset and key_pressed.char == prev_char:
            # what if we accidentally obey punctuation when we don't need it? Skip to next, not an error!
            pass
        else:
            print(key_pressed.char)
            curr_error.set(curr_error.get()+1)
    binder(check, charset)
    retry_butt['image'] = tp_tk
    for _ in text:
        next_char = text_field.get("insert", "insert+1c")
        prev_char = text_field.get("insert-1c", "insert")
        # this step takes care of punctuation according to our settings
        if next_char in markset and settings[0]:
            # as we skip this step, it shouldn't count
            c_counter -= 1
        else:
            # stop, wait until curr_succ variable changes (False->True) i.e. until we will have got a correct key
            tic = time.perf_counter()
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
        # exit when the text doesn't fit text_field and we can't see any more characters
        if c_counter == 40*3:
            break
    # prevent user from typing any further, 2 lines could be deleted with a SAME gain but this way is more stable
    binder(check, mode=False)
    # tempo calculations (with errors)
    average_cps = (len(text) - 1 - curr_error.get())/c_time
    relative_cps = 100*average_cps/TOP_CPS
    window.scv.set(round(relative_cps))
    if relative_cps >= 90:
        retry_butt['image'] = icon_tk
        global em
        em = True
    else:
        retry_butt['image'] = rfr_tk


head_label = Label(window, text="Start typing the line below:", font=main_font, bg=main_color)
head_label.grid(row=0, column=0, columnspan=2, pady=5)

text_field = Text(window, bg=focus_color, fg=text_color_a, height=3, width=40, font=main_font, relief=SUNKEN)
text_field.focus_set()
text_field.grid(row=1, column=0, columnspan=2, padx=18)

window.scv = IntVar()
w2 = Scale(window, from_=0, to=100, tickinterval=25, orient=HORIZONTAL, length=400, state=DISABLED, showvalue=False,
           font=main_font, label=f'CPS Rate (%, relative to {TOP_CPS})', variable=window.scv,
           troughcolor=focus_color, highlightbackground=main_color, bg=main_color)
w2.grid(row=2, column=0, sticky=N+S+W+E, padx=15)

rfr_tk = ImageTk.PhotoImage(rfr)
tp_tk = ImageTk.PhotoImage(tp)
# et = "You woke up one day with a dream... Harem full of demon girls."
retry_butt = Button(text='Retry', image=rfr_tk, command=lambda: text_handler(EXAMPLE), bg=main_color)
retry_butt.grid(row=2, column=1, sticky=N+S+W, ipadx=5, pady=10, rowspan=2)


setup_container = Frame(window)
setup_container.grid(row=3, column=0)
s1 = BooleanVar()
s1.set(True)
set1 = Checkbutton(setup_container, text="Auto punctuation", selectcolor=focus_color, background=main_color, variable=s1
                   , onvalue=True, offvalue=False, bg=main_color)
set1.grid(row=0, column=0)
s2 = BooleanVar()
set2 = Checkbutton(setup_container, text="Case sensitive", selectcolor=focus_color, background=main_color, variable=s2
                   , onvalue=True, offvalue=False)
set2.grid(row=0, column=1)

if __name__ == "__main__":
    text_handler(EXAMPLE)

window.mainloop()
