import os
import tkinter as tk
from tkinter import messagebox
import numpy as np

# Initialize main window
root = tk.Tk()
root.title("NGG")
root.geometry("500x400")  # Starting window size

# Start in normal windowed mode
root.attributes('-fullscreen', False)  # Ensure it starts windowed

def exit_fullscreen(event=None):
    """Exit full-screen mode when Escape key is pressed."""
    root.attributes('-fullscreen', False)

# Bind the Escape key to exit full-screen
root.bind('<Escape>', exit_fullscreen)

# Initialize a cache for preloaded fullscreen background
fullscreen_bg_photo = None

# Create the main frame for the UI
main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill="both", expand=True)

# Background label (empty initially)
bg_label = tk.Label(main_frame)

def toggle_fullscreen(event=None):
    """Toggle fullscreen mode on and off."""
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))

def calculate_font_size():
    width = root.winfo_width()
    height = root.winfo_height()
    return int(min(width, height) / 30)


def clear_screen():
    for widget in main_frame.winfo_children():
        if widget != bg_label:
            widget.pack_forget()
            widget.place_forget()


# Define the initial design dimensions
INITIAL_WIDTH = 500
INITIAL_HEIGHT = 400

# Set the geometry (this will be overridden by fullscreen, but we still keep the numbers for calculations)
root.geometry(f"{INITIAL_WIDTH}x{INITIAL_HEIGHT}")


def calculate_font_size():
    # Use the fixed dimensions for calculation instead of the current window size
    return int(min(INITIAL_WIDTH, INITIAL_HEIGHT) / 30)


def show_welcome_screen():
    clear_screen()

    frame = tk.Frame(main_frame, bg="black", bd=3)  # Reduced border size
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Keep centered

    font_size = calculate_font_size()

    label = tk.Label(frame, text="Welcome to the Number Guessing Game!", fg="white", bg="black",
                     font=("Arial", font_size, "bold"), wraplength=0)  # No wrapping initially
    label.pack(pady=5)  # Smaller padding

    def start_game():
        frame.destroy()  # Completely remove the frame
        select_num_players()  # Proceed to the next screen

    start_button = tk.Button(frame, text="Start", command=start_game, bg="#FFD700", fg="black",
                             font=("Arial", font_size), width=8, height=1)  # Smaller button
    start_button.pack(pady=20)

    def adjust_layout(event):
        """Adjusts frame and text dynamically when window resizes."""
        if not frame.winfo_exists():  # Check if frame exists
            return

        window_width = root.winfo_width()

        if window_width >= 1200:
            if label.winfo_exists():  # Check if label exists
                label.config(wraplength=0)
            frame.config(padx=10, pady=5)
        else:
            if label.winfo_exists():
                label.config(wraplength=window_width - 50)
            frame.config(padx=30, pady=20)

        # Adjust font size dynamically
        new_font_size = max(20, int(window_width / 45))

        if label.winfo_exists():
            label.config(font=("Arial", new_font_size, "bold"))
        if start_button.winfo_exists():
            start_button.config(font=("Arial", new_font_size))

        frame.place(relx=0.5, rely=0.5, anchor="center")

    root.bind("<Configure>", adjust_layout)

    root.update_idletasks()
    adjust_layout(None)

def start_game(level):
    global number, lowest_num, highest_num, current_turn, attempts

    current_turn = 0
    attempts = {name: 0 for name in player_names}

    if level == 1:
        lowest_num, highest_num = 1, 20
    elif level == 2:
        lowest_num, highest_num = 1, 50
    elif level == 3:
        lowest_num, highest_num = 1, 100

    number = np.random.randint(lowest_num, highest_num + 1)  # Add +1 to include highest_num

    show_guessing_screen()


def create_back_button(parent):
    """Creates a styled back button."""
    return tk.Button(parent, text="⬅ Back", command=go_back, bg="green", fg="white",
                     font=("Arial", 16), width=10)


import numpy as np

congratulatory_messages = [
    "Congrats!", "Kudos!", "Superb!", "Brilliant!", "Great!",
    "Champee!", "Best In The World!", "Bazenga!", "Mkuu!"
]


screen_history = []  # Stores previous screens

def navigate_to(screen_function):
    """Navigate to a new screen and store the current screen in history."""
    if screen_history and screen_history[-1] == screen_function:
        return  # Avoid duplicate entries in history
    screen_history.append(screen_function)
    screen_function()


def go_back():
    """Return to the previous screen, ensuring proper navigation."""
    if len(screen_history) > 1:
        screen_history.pop()  # Remove the current screen
        previous_screen = screen_history[-1]  # Get the last visited screen

        # Navigate back to the correct screen
        if previous_screen == show_level_selection:
            show_level_selection()
        elif previous_screen == show_player_input:
            show_player_input()
        elif previous_screen == select_num_players:
            select_num_players()
        elif previous_screen == show_guessing_screen:
            show_guessing_screen()
        else:
            previous_screen()  # General fallback for any other screen


def reset_game():
    show_welcome_screen()  # Goes back to the main menu


def show_guessing_screen():
    """Display the guessing game screen."""
    navigate_to(show_guessing_screen)  # Track this screen
    clear_screen()


    frame = tk.Frame(main_frame, bg="black", bd=5)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    font_size = calculate_font_size() * 2
    small_font_size = max(18, font_size // 2)

    # Create a full-frame container to center elements
    frame = tk.Frame(main_frame, bg="black", bd=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    # Guessing prompt with dynamic wrapping
    guess_label = tk.Label(
        frame,
        text=f"Guess a number between {lowest_num} and {highest_num}",
        fg="white", bg="black",
        font=("Arial", font_size),
        wraplength=main_frame.winfo_width() - 40
    )
    guess_label.pack(pady=10)

    # Update wraplength and reposition when window resizes
    def update_layout(event):
        guess_label.config(wraplength=event.width - 40)  # Adjust text wrapping
        frame.place(relx=0.5, rely=0.5, anchor="center")  # Ensure frame stays centered

    main_frame.bind("<Configure>", update_layout)  # Bind resize event

    player_label = tk.Label(frame, text=f"{player_names[current_turn]}'s turn",
                            fg="yellow", bg="black", font=("Arial", font_size))
    player_label.pack(pady=3)

    guess_entry = tk.Entry(frame, font=("Arial", font_size))
    guess_entry.pack(pady=3)
    guess_entry.focus_set()

    # Feedback label with dynamic font size adjustment
    feedback_label = tk.Label(
        frame, text="", fg="red", bg="black",
        font=("Arial", font_size)  # Default font size
    )
    feedback_label.pack(pady=3)

    # Function to adjust font size dynamically
    def update_feedback_font(event):
        new_font_size = max(10, event.width // 30)  # Adjust scaling factor for better readability
        feedback_label.config(font=("Arial", new_font_size))

    # Bind window resize event
    main_frame.bind("<Configure>", update_feedback_font)

    def check_guess(event=None):
        global current_turn

        guess = guess_entry.get().strip()
        if not guess.isdigit():
            feedback_label.config(text="Invalid Input! Enter a number.")
            return

        guess = int(guess)
        if guess < lowest_num or guess > highest_num:
            feedback_label.config(
                text=f"Out of range! Enter between {lowest_num} and {highest_num}",
                wraplength=main_frame.winfo_width() - 40  # Adjust based on window size
            )
            return

        player_name = player_names[current_turn]
        attempts[player_name] += 1

        if guess < number:
            feedback_label.config(text="Too low! Try again.")
        elif guess > number:
            feedback_label.config(text="Too high! Try again.")
        else:
               show_replay_popup(f"{player_name} guessed it right!")


        current_turn = (current_turn + 1) % num_players
        player_label.config(text=f"{player_names[current_turn]}'s turn")
        guess_entry.delete(0, tk.END)

    # Ensure the wraplength updates dynamically when resizing the window
    def update_feedback_wrap(event):
        feedback_label.config(wraplength=event.width - 40)

    main_frame.bind("<Configure>", update_feedback_wrap)  # Adjust on resize

    # Create a subframe for Quit and Back buttons on the same line
    button_frame = tk.Frame(frame, bg="black")
    button_frame.pack(pady=5)

    quit_button = tk.Button(button_frame, text="Quit", command=root.quit, bg="red", fg="white",
                            font=("Arial", small_font_size))
    quit_button.pack(side="left", padx=5)

    # create_back_button returns a button already; pass button_frame as its parent
    back_button = create_back_button(button_frame)
    back_button.pack(side="left", padx=5)

    guess_entry.bind("<Return>", check_guess)

def show_replay_popup(message):
    """Show replay popup with options to replay, go back, or quit."""
    popup = tk.Toplevel(root)
    random_message = np.random.choice(congratulatory_messages)  # Use NumPy's random.choice()
    popup.title(f'{random_message}')
    popup.configure(bg="black")

    tk.Label(popup, text=message, font=("Arial", 18, "bold"), fg="white", bg="black").pack(pady=10)

    def replay():
        popup.destroy()
        reset_game()

    replay_button = tk.Button(popup, text="Replay", font=("Arial", 16, "bold"), bg="green", fg="white", command=replay)
    replay_button.pack(pady=10)



    quit_button = tk.Button(popup, text="Quit", font=("Arial", 14), bg="red", fg="white", command=root.quit)
    quit_button.pack(pady=5)

def show_custom_message(title, message, message_type="info", on_close=None):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.configure(bg="black")

    # Get the current window size and position
    root.update_idletasks()  # Ensure we have the latest dimensions
    width = root.winfo_width()
    height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    # Ensure popup size is proportional but not too big
    popup_width = max(300, int(width * 0.5))  # 50% of main window width, min 300px
    popup_height = max(200, int(height * 0.3))  # 30% of main window height, min 200px

    if root.attributes("-fullscreen"):  # If in fullscreen mode
        popup_width = int(width * 0.2)  # 20% width
        popup_height = int(height * 0.13) # 13% height

    # Detect if the window is in fullscreen
    is_fullscreen = root.attributes("-fullscreen")

    # Adjust font sizes dynamically
    if is_fullscreen:
        title_font_size = max(12, int(min(width, height) / 70))  # Larger for fullscreen
        message_font_size = max(14, int(min(width, height) / 70))
    else:
        # Adjust font sizes dynamically based on window size
        title_font_size = max(14, int(min(width, height) / 40))  # Adjusted for smaller windows
        message_font_size = max(18, int(min(width, height) / 60))

    # Ensure popup stays inside the main window
    x_position = root_x + (width - popup_width) // 2
    y_position = root_y + (height - popup_height) // 2
    x_position = max(root_x, x_position)
    y_position = max(root_y, y_position)

    popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")


    # Determine text and background colors
    text_color = "white" if message_type == "info" else "red"

    # Title Label
    title_label = tk.Label(popup, text=title, fg="gold", bg="black",
                           font=("Arial", title_font_size, "bold"))
    title_label.pack(pady=(10, 5))

    # Message Label
    message_label = tk.Label(popup, text=message, fg=text_color, bg="black",
                             font=("Arial", message_font_size), wraplength=popup_width - 40)
    message_label.pack(pady=5, padx=15)

    # Function to close the popup
    def close_popup(event=None):
        popup.destroy()
        if on_close:
            on_close()

    # OK Button
    close_button = tk.Button(popup, text="OK", command=close_popup,
                             bg="#FFD700", fg="black", font=("Arial", message_font_size, "bold"),
                             width=8, height=1)
    close_button.pack(pady=10)

    popup.bind("<Return>", close_popup)  # Bind Enter key to close popup
    popup.transient(root)  # Attach popup to main window
    popup.grab_set()  # Modal popup
    root.wait_window(popup)  # Wait for it to close

def select_num_players():
    navigate_to(select_num_players)  # Track this screen
    clear_screen()


    frame = tk.Frame(main_frame, bg="black", bd=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    font_size = calculate_font_size() * 2

    tk.Label(frame, text="Select Number of Players", fg="white", bg="black", font=("Arial", font_size)).pack(pady=10)

    def set_players(n):
        global num_players
        num_players = n
        show_player_input()

    for i in range(1, 5):
        tk.Button(frame, text=f"{i} Player{'s' if i > 1 else ''}", command=lambda n=i: set_players(n), bg="#008CBA",
                  fg="white", font=("Arial", font_size), width=15).pack(pady=5)


def show_player_input():
    navigate_to(show_player_input)  # Track this screen
    clear_screen()


    frame = tk.Frame(main_frame, bg="black", bd=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    font_size = calculate_font_size() * 2
    small_font_size = max(18, font_size // 2)

    tk.Label(frame, text="Enter Player Names", fg="white", bg="black", font=("Arial", font_size)).pack(pady=10)

    entries = []

    def submit_names():
        global player_names
        player_names = [entry.get().strip() for entry in entries]
        if any(name == "" for name in player_names):
            show_custom_message("Invalid Input", "All player names must be entered.")
            return
        show_level_selection()

    for i in range(num_players):
        entry = tk.Entry(frame, font=("Arial", font_size))
        entry.pack(pady=5)
        entry.insert(0, f"Player {i + 1}")
        entries.append(entry)

    # Create a subframe to hold the buttons on the same line
    button_frame = tk.Frame(frame, bg="black")
    button_frame.pack(pady=10)

    continue_button = tk.Button(button_frame, text="Continue", command=submit_names, bg="#008CBA", fg="white",
                                font=("Arial", small_font_size), width=10)
    continue_button.pack(side="right", padx=5)

    back_button = tk.Button(button_frame, text="⬅ Back", command=go_back, bg="blue", fg="white",
                            font=("Arial", small_font_size), width=10)
    back_button.pack(side="left", padx=5)


def show_custom_range_input():
    navigate_to(show_custom_range_input)  # Track this screen
    clear_screen()


    frame = tk.Frame(main_frame, bg="black", bd=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    font_size = calculate_font_size() * 2
    small_font_size = max(20, font_size // 2)

    tk.Label(frame, text="Enter Your Custom Range", fg="white", bg="black",
             font=("Arial", font_size)).pack(pady=10)

    low_label = tk.Label(frame, text="Lowest Number:", fg="white", bg="black",
                         font=("Arial", font_size))
    low_label.pack(pady=5)

    low_entry = tk.Entry(frame, font=("Arial", font_size))
    low_entry.pack(pady=5)

    high_label = tk.Label(frame, text="Highest Number:", fg="white", bg="black",
                          font=("Arial", font_size))
    high_label.pack(pady=5)

    high_entry = tk.Entry(frame, font=("Arial", font_size))
    high_entry.pack(pady=5)

    def set_range():
        global lowest_num, highest_num, number, current_turn, attempts

        lowest = low_entry.get().strip()
        highest = high_entry.get().strip()

        if not (lowest.isdigit() and highest.isdigit()):
            show_custom_message("Invalid Input", "Please enter valid numbers.")
            return

        lowest_num, highest_num = int(lowest), int(highest)

        if lowest_num >= highest_num:
            show_custom_message("Invalid Range", "Lowest number must be smaller than highest number.")
            return

        number = np.random.randint(lowest_num, highest_num)
        current_turn = 0  # Initialize current_turn before using it
        attempts = {name: 0 for name in player_names}  # Initialize attempts

        show_guessing_screen()

    # Create a subframe to hold the buttons on the same line
    button_frame = tk.Frame(frame, bg="black")
    button_frame.pack(pady=10)

    submit_button = tk.Button(button_frame, text="Start Game", command=set_range, bg="#008CBA", fg="white",
                              font=("Arial", small_font_size))
    submit_button.pack(side="right", padx=5)

    back_button = tk.Button(button_frame, text="⬅ Back", command=go_back, bg="blue", fg="white",
                            font=("Arial", small_font_size), width=10)
    back_button.pack(side="left", padx=5)


def show_level_selection():
    navigate_to(show_level_selection)  # Track this screen
    clear_screen()


    frame = tk.Frame(main_frame, bg="black", bd=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    font_size = calculate_font_size() * 2
    small_font_size = max(18, font_size // 2)

    tk.Label(frame, text="Select Difficulty Level", fg="white", bg="black",
             font=("Arial", font_size)).pack(pady=10)

    levels = ["Easy (1-20)", "Medium (1-50)", "Hard (1-100)", "Own Range"]
    for level, text in enumerate(levels, start=1):
        if text == "Own Range":
            tk.Button(frame, text=text, command=show_custom_range_input, bg="#008CBA", fg="white",
                      font=("Arial", font_size)).pack(pady=5)
        else:
            tk.Button(frame, text=text, command=lambda lvl=level: start_game(lvl), bg="#008CBA", fg="white",
                      font=("Arial", font_size)).pack(pady=5)

    # Create a subframe for the Back and Quit buttons on the same line
    button_frame = tk.Frame(frame, bg="black")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="⬅ Back", command=go_back, bg="blue", fg="white",
              font=("Arial", small_font_size), width=10).pack(side="left", padx=5)

    tk.Button(button_frame, text="Quit", command=root.quit, bg="red", fg="white",
              font=("Arial", small_font_size), width=10).pack(side="left", padx=5)



root.bind("<F11>", toggle_fullscreen)

show_welcome_screen()
root.mainloop()
