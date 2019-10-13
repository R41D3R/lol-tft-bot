from pynput import keyboard
import pyautogui

from controller.bot.bot import Bot


running = False


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    global running
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        running = False


user_action = pyautogui.confirm("The bot has been started. Press Ok to continue.\n"
                                "WARNING: Don't type sensible Informations while the bot is running")
if user_action == "OK":
    bot = Bot()
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    running = True
    while running:
        pass
else:
    pass
