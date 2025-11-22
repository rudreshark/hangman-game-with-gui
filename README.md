# Hangman Game (Python GUI)

This is an interactive Hangman game built with Python and a graphical user interface (GUI) using Tkinter. Players must guess a secret word one letter at a time, with each incorrect guess drawing part of the hangman illustration. With difficulty levels and categories for Fruits or Vegetables, this is a fun and challenging word game for all ages.

## Features

- Beautiful, user-friendly GUI with a colorful theme
- Choose difficulty and word category (Fruits, Vegetables, Mixed)
- Real-time hangman drawing as the game progresses
- Full-word or single-letter guesses
- Hint button to reveal an unguessed letter
- Pause/Resume (ESC), Instructions & Credits screens
- Works on Windows, macOS, and Linux

## Requirements

- Python 3.7 or later
- Tkinter (`tkinter` is usually included with Python installations)
- No external packages required

## How to Install & Run (All Platforms)

### Step 1: Download or Clone the Repository

#### Using Git:
```bash
git clone https://github.com/rudreshark/hangman-game-with-gui.git
cd hangman-game-with-gui
```
#### Or download ZIP:
- Click "Code" > "Download ZIP" on the repo page.
- Extract the ZIP file.

### Step 2: Install Python (if you don't have it)

#### Windows:
- Download Python from [python.org/downloads](https://www.python.org/downloads/windows/)
- Run the installer, **check "Add Python to PATH"**.

#### macOS:
- Python 3 usually comes pre-installed.
- Or install via Homebrew:
  ```bash
  brew install python
  ```

#### Linux:
- Install via your package manager, e.g.:
  ```bash
  sudo apt update
  sudo apt install python3 python3-tk
  ```
  (For most distros, `python3-tk` brings in Tkinter.)

### Step 3: Run the Hangman Game

```bash
python hangman_gui.py
```
- If you have multiple python versions, use:
  ```bash
  python3 hangman_gui.py
  ```

Game window should launch automatically!

---

## Troubleshooting

- **Tkinter errors**: If you get an error about `tkinter` not found, install it via your package manager (Linux: `sudo apt install python3-tk`, macOS: Homebrew comes with Tkinter, Windows: bundled in Python installer).
- **Python not found**: Make sure Python is installed and added to your PATH.

---

## License

MIT License

---

Perfect for beginners and word puzzle fans, this GUI-based Hangman game is a fun way to challenge your vocabulary skills.
