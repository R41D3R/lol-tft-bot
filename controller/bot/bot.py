import time
import logging

import pyautogui


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Bot:
    def __init__(self):
        self.key_wait_time = 0.2
        logger.info("Bot has been started.")

    @property
    def _screenshot(self):
        return pyautogui.screenshot()

    @property
    def _position(self):
        return pyautogui.position()

    @property
    def _screen_size(self):
        return pyautogui.size()

    def __str__(self):
        return f"Bot position: {self._position} on screen with size: {self._screen_size}"

    @staticmethod
    def move_to(x, y, duration):
        pyautogui.moveTo(x, y, duration=duration)

    @staticmethod
    def _is_valid_xy(x, y):
        return pyautogui.onScreen(x, y)

    @staticmethod
    def _click():
        pyautogui.click()

    @staticmethod
    def press_keys(keys):
        pyautogui.hotkey(*keys)

    @staticmethod
    def _save_screenshot(file_name, directory="./"):
        pyautogui.screenshot(directory + file_name + ".png")

    def _press_key(self, key_name):
        pyautogui.keyDown(key_name)
        time.sleep(self.key_wait_time)
        pyautogui.keyUp(key_name)
        time.sleep(self.key_wait_time)


