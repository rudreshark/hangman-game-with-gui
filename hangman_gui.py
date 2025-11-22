import tkinter as tk
from tkinter import messagebox
import random
import string

# Word lists 

easy_fruits = [
    "apple", "banana", "orange", "grape", "strawberry",
    "watermelon", "mango", "pineapple", "pear", "peach"
]

easy_vegetables = [
    "cucumber", "potato", "carrot", "onion", "sweet potato",
    "garlic", "beetroot"
]

medium_fruits = [
    "kiwifruit", "passion", "pomegranate", "jackfruit", "star fruit"
]

medium_vegetables = [
    "cauliflower", "broccoli", "cabbage", "mushrooms", "cucumber",
    "drumstick", "ladies finger", "sweet potato", "green chilli", "beans"
]

hard_fruits = [
    "lychee", "pineapple", "dragon fruit", "pomegranate", "guava",
    "chikoo", "plum", "blackcurrant", "rambutan", "longan", "sapodilla"
]

hard_vegetables = [
    "baby corn", "ginger", "millet", "turmeric", "pumpkin",
    "asparagus", "artichoke", "zucchini", "radicchio", "kohlrabi"
]

extreme_fruits = [
    "ice apple", "jamun", "wood apple",  "avocado",  "miraclefruit"
]

extreme_vegetables = [
    "elephant foot", "bottle gourd", "drumsticks",
    "bitter gourd", "spring onion", "broccoli"
]


def normalize_list(words):
    seen = set()
    out = []
    for w in words:
        w2 = " ".join(w.lower().strip().split())
        if w2 not in seen:
            seen.add(w2)
            out.append(w2)
    return out


easy_fruits = normalize_list(easy_fruits)
easy_vegetables = normalize_list(easy_vegetables)
medium_fruits = normalize_list(medium_fruits)
medium_vegetables = normalize_list(medium_vegetables)
hard_fruits = normalize_list(hard_fruits)
hard_vegetables = normalize_list(hard_vegetables)
extreme_fruits = normalize_list(extreme_fruits)
extreme_vegetables = normalize_list(extreme_vegetables)


# Styling – Colorful Theme

BG = "#FFF8E1"
PANEL = "#FFE0B2"
ACCENT = "#FB8C00"
TEXT = "#4E342E"
BUTTON_BG = "#FFCC80"
BUTTON_HOVER = "#FFB74D"
ENTRY_BG = "#FFFFFF"

FONT_TITLE = ("Segoe UI", 28, "bold")
FONT_SUB = ("Segoe UI", 12)
FONT_TEXT = ("Segoe UI", 11)
FONT_WORD = ("Consolas", 26)


# Main application

class HangmanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Game")
        self.geometry("760x640")
        self.configure(bg=BG)
        self.resizable(False, False)

        # Shared state
        self.difficulty = tk.StringVar(value="Easy")
        self.category = tk.StringVar(value="Mixed")
        self.max_attempts = 6

        # Game state
        self.secret_word = ""
        self.guessed_letters = set()
        self.wrong_attempts = 0

        # track current frame name (for pause logic)
        self.current_frame_name = None

        # container frame
        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)

        # frames dictionary
        self.frames = {}

        # instantiate frames (include PauseScreen)
        for F in (MainMenu, DifficultyScreen, CategoryScreen, InstructionsScreen,
                  CreditsScreen, GameScreen, GameOverScreen, PauseScreen):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

        # key binding for ESC -> toggle pause
        self.bind("<Escape>", lambda e: self.toggle_pause())

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        self.current_frame_name = name

    def toggle_pause(self):
        # Only allow pausing when game is running
        if self.current_frame_name == "PauseScreen":
            # resume to previous game if available (go back to GameScreen)
            self.show_frame("GameScreen")
            # focus entry on resume
            gs: GameScreen = self.frames["GameScreen"]
            gs.entry.focus_set()
        elif self.current_frame_name == "GameScreen":
            self.show_frame("PauseScreen")

    def choose_word(self):
        d = self.difficulty.get()
        c = self.category.get()
        pool = []

        if d == "Easy":
            if c == "Fruits":
                pool = easy_fruits
            elif c == "Vegetables":
                pool = easy_vegetables
            else:
                pool = easy_fruits + easy_vegetables

        elif d == "Medium":
            if c == "Fruits":
                pool = medium_fruits or easy_fruits
            elif c == "Vegetables":
                pool = medium_vegetables or easy_vegetables
            else:
                pool = medium_fruits + medium_vegetables
                if not pool:
                    pool = easy_fruits + easy_vegetables

        elif d == "Hard":
            if c == "Fruits":
                pool = hard_fruits or medium_fruits or easy_fruits
            elif c == "Vegetables":
                pool = hard_vegetables or medium_vegetables or easy_vegetables
            else:
                pool = hard_fruits + hard_vegetables
                if not pool:
                    pool = medium_fruits + medium_vegetables

        elif d == "Extreme":
            if c == "Fruits":
                pool = extreme_fruits or hard_fruits or medium_fruits
            elif c == "Vegetables":
                pool = extreme_vegetables or hard_vegetables or medium_vegetables
            else:
                pool = extreme_fruits + extreme_vegetables
                if not pool:
                    pool = hard_fruits + hard_vegetables

        if not pool:
            pool = easy_fruits + easy_vegetables

        return random.choice(pool)

    def add_hover(self, button: tk.Button):
        """Add simple hover effect to a button (background color change)."""
        def on_enter(e):
            try:
                button["background"] = BUTTON_HOVER
            except tk.TclError:
                pass
        def on_leave(e):
            try:
                button["background"] = BUTTON_BG
            except tk.TclError:
                pass
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)


# Screens / Frames

class StyledFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        # common padding frame
        self.inner = tk.Frame(self, bg=BG)
        self.inner.pack(fill="both", expand=True, padx=20, pady=12)


class MainMenu(StyledFrame):
    def __init__(self, parent, controller: HangmanApp):
        super().__init__(parent, controller)

        title = tk.Label(self.inner, text="HANGMAN", font=FONT_TITLE, fg=TEXT, bg=BG)
        title.pack(pady=(10, 6))

        subtitle = tk.Label(self.inner, text="Fruits & Vegetables Edition", font=FONT_SUB, fg=TEXT, bg=BG)
        subtitle.pack(pady=(0, 12))

        # center panel
        panel = tk.Frame(self.inner, bg=PANEL, bd=0, relief="ridge")
        panel.pack(pady=8, ipadx=10, ipady=18)

        btn_start = tk.Button(panel, text="Start Game", font=FONT_SUB, bg=BUTTON_BG, fg=TEXT,
                              width=28, command=lambda: controller.show_frame("DifficultyScreen"))
        btn_start.pack(pady=8)
        controller.add_hover(btn_start)

        btn_instructions = tk.Button(panel, text="Instructions", font=FONT_SUB, bg=BUTTON_BG, fg=TEXT,
                                     width=28, command=lambda: controller.show_frame("InstructionsScreen"))
        btn_instructions.pack(pady=6)
        controller.add_hover(btn_instructions)

        btn_credits = tk.Button(panel, text="Credits", font=FONT_SUB, bg=BUTTON_BG, fg=TEXT,
                                width=28, command=lambda: controller.show_frame("CreditsScreen"))
        btn_credits.pack(pady=6)
        controller.add_hover(btn_credits)

        btn_exit = tk.Button(panel, text="Exit", font=FONT_SUB, bg=BUTTON_BG, fg=TEXT,
                             width=28, command=self.quit_app)
        btn_exit.pack(pady=6)
        controller.add_hover(btn_exit)

        footer = tk.Label(self.inner, text="Tip: Press ESC to pause during the game.", font=("Segoe UI", 10),
                          fg=TEXT, bg=BG)
        footer.pack(side="bottom", pady=10)

    def quit_app(self):
        self.controller.quit()


class DifficultyScreen(StyledFrame):
    def __init__(self, parent, controller: HangmanApp):
        super().__init__(parent, controller)

        label = tk.Label(self.inner, text="Select Difficulty", font=("Segoe UI", 20, "bold"), fg=TEXT, bg=BG)
        label.pack(pady=(6, 8))

        opts = ["Easy", "Medium", "Hard", "Extreme"]
        btns = tk.Frame(self.inner, bg=BG)
        btns.pack(pady=6)
        for opt in opts:
            tk.Radiobutton(btns, text=opt, variable=controller.difficulty, value=opt,
                           font=FONT_SUB, bg=BG, fg=TEXT, selectcolor=PANEL).pack(anchor="w", padx=8, pady=3)

        nav = tk.Frame(self.inner, bg=BG)
        nav.pack(pady=16)
        btn_back = tk.Button(nav, text="Back", font=FONT_SUB, bg=BUTTON_BG, command=lambda: controller.show_frame("MainMenu"))
        btn_back.pack(side="left", padx=8)
        controller.add_hover(btn_back)

        btn_next = tk.Button(nav, text="Next", font=FONT_SUB, bg=BUTTON_BG, command=lambda: controller.show_frame("CategoryScreen"))
        btn_next.pack(side="left", padx=8)
        controller.add_hover(btn_next)


class CategoryScreen(StyledFrame):
    def __init__(self, parent, controller: HangmanApp):
        super().__init__(parent, controller)

        label = tk.Label(self.inner, text="Select Category", font=("Segoe UI", 20, "bold"), fg=TEXT, bg=BG)
        label.pack(pady=(6, 8))

        opts = [("Fruits", "Fruits"), ("Vegetables", "Vegetables"), ("Mixed", "Mixed")]
        frame = tk.Frame(self.inner, bg=BG)
        frame.pack(pady=6)
        for text, val in opts:
            tk.Radiobutton(frame, text=text, variable=controller.category, value=val,
                           font=FONT_SUB, bg=BG, fg=TEXT, selectcolor=PANEL).pack(anchor="w", padx=8, pady=3)

        nav = tk.Frame(self.inner, bg=BG)
        nav.pack(pady=16)
        btn_back = tk.Button(nav, text="Back", font=FONT_SUB, bg=BUTTON_BG,
                  command=lambda: controller.show_frame("DifficultyScreen"))
        btn_back.pack(side="left", padx=8)
        controller.add_hover(btn_back)

        btn_start = tk.Button(nav, text="Start Game", font=FONT_SUB, bg=BUTTON_BG,
                  command=self.start_game)
        btn_start.pack(side="left", padx=8)
        controller.add_hover(btn_start)

    def start_game(self):
        game_frame: GameScreen = self.controller.frames["GameScreen"]
        game_frame.setup_new_game()
        self.controller.show_frame("GameScreen")
        game_frame.entry.focus_set()


class InstructionsScreen(StyledFrame):
    def __init__(self, parent, controller: HangmanApp):
        super().__init__(parent, controller)

        title = tk.Label(self.inner, text="Instructions", font=("Segoe UI", 18, "bold"), fg=TEXT, bg=BG)
        title.pack(pady=6)

        text = (
            "• Choose difficulty and category (Fruits / Vegetables / Mixed).\n"
            "• Guess one letter at a time or try the full-word guess.\n"
            "• You have 6 wrong attempts (head / body / arms / legs etc.).\n"
            "• Multi-word answers show spaces — you don't need to guess spaces.\n"
            "• Use the 'Reveal 1 letter' hint if needed (it reveals an unguessed letter).\n"
            "• Press Enter to submit a guess quickly. Press ESC to pause."
        )
        tk.Label(self.inner, text=text, font=FONT_TEXT, fg=TEXT, bg=BG, justify="left").pack(padx=6, pady=10)

        btn_back = tk.Button(self.inner, text="Back to Menu", font=FONT_SUB, bg=BUTTON_BG,
                  command=lambda: controller.show_frame("MainMenu"))
        btn_back.pack(pady=8)
        controller.add_hover(btn_back)


class CreditsScreen(StyledFrame):
    def __init__(self, parent, controller: HangmanApp):
        super().__init__(parent, controller)
        title = tk.Label(self.inner, text="Credits", font=("Segoe UI", 18, "bold"), fg=TEXT, bg=BG)
        title.pack(pady=6)
        text = "Created by: Team No.150 \n Project: Hangman Game With GUI "
        tk.Label(self.inner, text=text, font=FONT_TEXT, fg=TEXT, bg=BG).pack(pady=10)
        btn_back = tk.Button(self.inner, text="Back to Menu", font=FONT_SUB, bg=BUTTON_BG,
                  command=lambda: controller.show_frame("MainMenu"))
        btn_back.pack(pady=8)
        controller.add_hover(btn_back)


# Game Canvas Drawing (no images)

class HangmanDrawer:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.reset()

    def reset(self):
        self.canvas.delete("all")
        w = int(self.canvas["width"])
        h = int(self.canvas["height"])
        base_y = h - 30
        self.canvas.create_line(40, base_y, 160, base_y, width=4)   # ground
        self.canvas.create_line(100, base_y, 100, 50, width=4)      # vertical pole
        self.canvas.create_line(100, 50, 260, 50, width=4)          # top beam
        self.canvas.create_line(260, 50, 260, 90, width=4)          # rope
        self.parts = {
            "head": None,
            "body": None,
            "left_arm": None,
            "right_arm": None,
            "left_leg": None,
            "right_leg": None
        }

    def draw_stage(self, stage: int):
        if stage <= 0:
            return
        if stage >= 1 and not self.parts["head"]:
            self.parts["head"] = self.canvas.create_oval(230, 90, 290, 150, width=3)
        if stage >= 2 and not self.parts["body"]:
            self.parts["body"] = self.canvas.create_line(260, 150, 260, 260, width=3)
        if stage >= 3 and not self.parts["left_arm"]:
            self.parts["left_arm"] = self.canvas.create_line(260, 170, 220, 210, width=3)
        if stage >= 4 and not self.parts["right_arm"]:
            self.parts["right_arm"] = self.canvas.create_line(260, 170, 300, 210, width=3)
        if stage >= 5 and not self.parts["left_leg"]:
            self.parts["left_leg"] = self.canvas.create_line(260, 260, 230, 320, width=3)
        if stage >= 6 and not self.parts["right_leg"]:
            self.parts["right_leg"] = self.canvas.create_line(260, 260, 290, 320, width=3)


# Game Screen

class GameScreen(StyledFrame):
    def __init__(self, parent, controller: HangmanApp):
        super().__init__(parent, controller)

        top = tk.Frame(self.inner, bg=BG)
        top.pack(fill="x", pady=(6, 8))
        tk.Label(top, text="Hangman", font=("Segoe UI", 20, "bold"), fg=TEXT, bg=BG).pack(side="left")
        self.info_label = tk.Label(top, text="", font=FONT_SUB, fg=TEXT, bg=BG)
        self.info_label.pack(side="right", padx=8)

        # center frame with canvas and word
        center = tk.Frame(self.inner, bg=BG)
        center.pack(fill="both", expand=True)

        # Hangman canvas
        canvas_frame = tk.Frame(center, bg=BG)
        canvas_frame.pack(side="left", padx=12)
        self.canvas = tk.Canvas(canvas_frame, width=360, height=380, bg="white", bd=0, highlightthickness=0)
        self.canvas.pack()
        self.drawer = HangmanDrawer(self.canvas)

        # right panel with progress and controls
        right = tk.Frame(center, bg=BG)
        right.pack(side="left", fill="y", padx=8)

        tk.Label(right, text="Word:", font=("Segoe UI", 12), fg=TEXT, bg=BG).pack(anchor="w", pady=(6, 2))
        self.word_label = tk.Label(right, text="", font=FONT_WORD, fg=TEXT, bg=BG, wraplength=300, justify="left")
        self.word_label.pack(anchor="w", pady=(0, 12))

        tk.Label(right, text="Enter letter or full word:", font=FONT_SUB, fg=TEXT, bg=BG).pack(anchor="w")
        self.entry = tk.Entry(right, font=("Segoe UI", 14), width=22, justify="center", bg=ENTRY_BG)
        self.entry.pack(pady=6)
        self.entry.bind("<Return>", lambda e: self.submit_guess())

        btns = tk.Frame(right, bg=BG)
        btns.pack(pady=8)
        self.guess_btn = tk.Button(btns, text="Guess", font=FONT_SUB, bg=BUTTON_BG, command=self.submit_guess)
        self.guess_btn.pack(side="left", padx=6)
        controller.add_hover(self.guess_btn)

        self.hint_btn = tk.Button(btns, text="Reveal 1 letter", font=FONT_SUB, bg=BUTTON_BG, command=self.reveal_one_letter)
        self.hint_btn.pack(side="left", padx=6)
        controller.add_hover(self.hint_btn)

        self.restart_btn = tk.Button(btns, text="Restart", font=FONT_SUB, bg=BUTTON_BG, command=self.setup_new_game)
        self.restart_btn.pack(side="left", padx=6)
        controller.add_hover(self.restart_btn)

        self.message_label = tk.Label(right, text="", font=FONT_SUB, fg=TEXT, bg=BG, wraplength=240, justify="left")
        self.message_label.pack(pady=8)

        self.guessed_label = tk.Label(right, text="Guessed: ", font=FONT_SUB, fg=TEXT, bg=BG, wraplength=240, justify="left")
        self.guessed_label.pack(pady=4)

        self.attempts_label = tk.Label(right, text="Attempts: 0/6", font=FONT_SUB, fg=TEXT, bg=BG)
        self.attempts_label.pack(pady=6)

        nav = tk.Frame(self.inner, bg=BG)
        nav.pack(pady=10)
        btn_back = tk.Button(nav, text="Back to Menu", font=FONT_SUB, bg=BUTTON_BG, command=self.back_to_menu)
        btn_back.pack(side="left", padx=6)
        controller.add_hover(btn_back)
        btn_change = tk.Button(nav, text="Change Category", font=FONT_SUB, bg=BUTTON_BG,
                  command=lambda: controller.show_frame("CategoryScreen"))
        btn_change.pack(side="left", padx=6)
        controller.add_hover(btn_change)

        # keyboard binding to focus entry on key press (letters)
        self.controller.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        # only focus for letter keys
        if event.char and event.char.lower() in string.ascii_lowercase:
            if not self.entry.focus_get():
                self.entry.focus_set()

    def setup_new_game(self):
        app: HangmanApp = self.controller
        app.secret_word = app.choose_word()
        app.guessed_letters = set()
        app.wrong_attempts = 0
        self.entry.delete(0, tk.END)
        self.update_ui_init()
        # draw blank scaffold
        self.drawer.reset()
        self.message_label.config(text="")

    def update_ui_init(self):
        app: HangmanApp = self.controller
        self.info_label.config(text=f"{app.difficulty.get()} | {app.category.get()}")
        self.update_word_display()
        self.guessed_label.config(text="Guessed: ")
        self.attempts_label.config(text=f"Attempts: {app.wrong_attempts}/{app.max_attempts}")
        self.guess_btn.config(state="normal")
        self.hint_btn.config(state="normal")

    def update_word_display(self):
        app: HangmanApp = self.controller
        display = []
        for ch in app.secret_word:
            if ch.isalpha():
                display.append(ch if ch in app.guessed_letters else "_")
            else:
                display.append(ch)  # reveal spaces/punctuation
        self.word_label.config(text=" ".join(display))

    def submit_guess(self):
        app: HangmanApp = self.controller

        # block input if not on GameScreen (pausing)
        if app.current_frame_name != "GameScreen":
            return

        guess = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)
        if not guess:
            self.message_label.config(text="Please enter a letter or full-word guess.")
            return

        # full-word guess
        if len(guess) > 1:
            normalized_guess = " ".join(guess.split())
            normalized_secret = " ".join(app.secret_word.split())
            if normalized_guess == normalized_secret:
                for c in app.secret_word:
                    if c.isalpha():
                        app.guessed_letters.add(c)
                self.update_word_display()
                self.message_label.config(text="🎉 Correct! You solved the word.")
                self.end_game(win=True)
            else:
                app.wrong_attempts += 1
                self.attempts_label.config(text=f"Attempts: {app.wrong_attempts}/{app.max_attempts}")
                self.drawer.draw_stage(app.wrong_attempts)
                self.message_label.config(text=f"Wrong word guess! ({app.wrong_attempts}/{app.max_attempts})")
                if app.wrong_attempts >= app.max_attempts:
                    self.end_game(win=False)
            self.update_guessed_label()
            return

        # single-letter guess
        letter = guess
        if len(letter) != 1 or not letter.isalpha():
            self.message_label.config(text="Enter a single alphabet letter or a full-word guess.")
            return

        if letter in app.guessed_letters:
            self.message_label.config(text=f"You already guessed '{letter}'.")
            return

        app.guessed_letters.add(letter)
        if letter in app.secret_word:
            self.update_word_display()
            self.update_guessed_label()
            all_done = all((ch in app.guessed_letters or not ch.isalpha()) for ch in app.secret_word)
            if all_done:
                self.message_label.config(text="🎉 You Won!")
                self.end_game(win=True)
            else:
                self.message_label.config(text=f"Nice! '{letter}' is in the word.")
        else:
            app.wrong_attempts += 1
            self.drawer.draw_stage(app.wrong_attempts)
            self.attempts_label.config(text=f"Attempts: {app.wrong_attempts}/{app.max_attempts}")
            self.update_guessed_label()
            self.message_label.config(text=f"Wrong guess '{letter}' ({app.wrong_attempts}/{app.max_attempts})")
            if app.wrong_attempts >= app.max_attempts:
                self.end_game(win=False)

    def update_guessed_label(self):
        app: HangmanApp = self.controller
        letters = sorted([c for c in app.guessed_letters if c.isalpha()])
        self.guessed_label.config(text="Guessed: " + (", ".join(letters) if letters else "-"))

    def reveal_one_letter(self):
        app: HangmanApp = self.controller

        # block hint if paused
        if app.current_frame_name != "GameScreen":
            return

        remaining = [c for c in set(app.secret_word) if c.isalpha() and c not in app.guessed_letters]
        if not remaining:
            self.message_label.config(text="No letters left to reveal.")
            return
        chosen = random.choice(remaining)
        app.guessed_letters.add(chosen)
        self.update_word_display()
        self.update_guessed_label()
        self.message_label.config(text=f"Hint: revealed '{chosen}'")
        all_done = all((ch in app.guessed_letters or not ch.isalpha()) for ch in app.secret_word)
        if all_done:
            self.end_game(win=True)

    def end_game(self, win: bool):
        app: HangmanApp = self.controller
        self.guess_btn.config(state="disabled")
        self.hint_btn.config(state="disabled")
        go_screen: GameOverScreen = app.frames["GameOverScreen"]
        go_screen.set_result(win, app.secret_word)
        app.show_frame("GameOverScreen")

    def back_to_menu(self):
        if messagebox.askyesno("Back to Menu", "Return to Main Menu? Current game will be lost."):
            self.controller.show_frame("MainMenu")


class GameOverScreen(StyledFrame):
    def __init__(self, parent, controller: HangmanApp):
        super().__init__(parent, controller)
        self.controller = controller
        title = tk.Label(self.inner, text="", font=("Segoe UI", 24, "bold"), fg=TEXT, bg=BG)
        title.pack(pady=12)
        self.title = title

        self.word_lbl = tk.Label(self.inner, text="", font=("Consolas", 20), fg=TEXT, bg=BG)
        self.word_lbl.pack(pady=8)

        btns = tk.Frame(self.inner, bg=BG)
        btns.pack(pady=12)
        btn_play = tk.Button(btns, text="Play Again (same settings)", font=FONT_SUB, bg=BUTTON_BG,
                  command=self.play_again)
        btn_play.pack(side="left", padx=8)
        controller.add_hover(btn_play)

        btn_home = tk.Button(btns, text="Main Menu", font=FONT_SUB, bg=BUTTON_BG,
                  command=lambda: controller.show_frame("MainMenu"))
        btn_home.pack(side="left", padx=8)
        controller.add_hover(btn_home)

        btn_change = tk.Button(btns, text="Change Category/Difficulty", font=FONT_SUB, bg=BUTTON_BG,
                  command=lambda: controller.show_frame("DifficultyScreen"))
        btn_change.pack(side="left", padx=8)
        controller.add_hover(btn_change)

    def set_result(self, win: bool, secret: str):
        if win:
            self.title.config(text="🎉 You Won! 🎉", fg="green")
        else:
            self.title.config(text="❌ You Lost ❌", fg="red")
        self.word_lbl.config(text=f"The word was: {secret}")

    def play_again(self):
        game_frame: GameScreen = self.controller.frames["GameScreen"]
        game_frame.setup_new_game()
        self.controller.show_frame("GameScreen")
        game_frame.entry.focus_set()


# Pause Screen (ESC)

class PauseScreen(StyledFrame):
    def __init__(self, parent, controller: HangmanApp):
        super().__init__(parent, controller)

        tk.Label(self.inner, text="⏸ PAUSED", font=("Segoe UI", 26, "bold"),
                 fg=TEXT, bg=BG).pack(pady=20)

        btn_resume = tk.Button(self.inner, text="Resume (ESC)", font=FONT_SUB,
                               bg=BUTTON_BG, command=self.resume)
        btn_resume.pack(pady=10)
        controller.add_hover(btn_resume)

        btn_main = tk.Button(self.inner, text="Main Menu", font=FONT_SUB,
                             bg=BUTTON_BG, command=lambda: controller.show_frame("MainMenu"))
        btn_main.pack(pady=10)
        controller.add_hover(btn_main)

    def resume(self):
        # simply go back to GameScreen
        self.controller.show_frame("GameScreen")
        # focus entry when resuming
        gs: GameScreen = self.controller.frames["GameScreen"]
        gs.entry.focus_set()

# App launch

if __name__ == "__main__":
    app = HangmanApp()
    # center the window on screen (optional)
    app.update_idletasks()
    width = app.winfo_width() or 760
    height = app.winfo_height() or 640
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")
    app.mainloop()
