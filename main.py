from tkinter import *
import pandas
import random

# -------------------------------- Constants & Globals -------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
BLACK = "#000000"
WHITE = "#FFFFFF"
TITLE_FONT = ("arial", 40, "italic")
WORD_FONT = ("arial", 60, "bold")
to_learn = {}
current_card = {}

# -------------------------------- Word List Updating Mechanism -------------------------------- #
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# -------------------------------- Card & Data Functions -------------------------------- #

def get_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(language, text="French", fill=BLACK)
    canvas.itemconfig(word, text=current_card["French"], fill=BLACK)
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(language, text="English", fill=WHITE)
    canvas.itemconfig(word, text=current_card["English"], fill=WHITE)


def remove_word():
    global current_card, flip_timer, to_learn
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    get_card()


# -------------------------------- UI Setup -------------------------------- #
window = Tk()
window.title("French Flashcards")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
language = canvas.create_text(400, 150, text="", font=TITLE_FONT, fill=BLACK)
word = canvas.create_text(400, 263, text="", font=WORD_FONT, fill=BLACK)
canvas.grid(row=0, column=0, columnspan=2)

wrong_button_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_button_img, highlightbackground=BACKGROUND_COLOR, command=get_card)
wrong_button.grid(row=1, column=0)

right_button_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_img, highlightbackground=BACKGROUND_COLOR, command=remove_word)
right_button.grid(row=1, column=1)

get_card()

window.mainloop()
