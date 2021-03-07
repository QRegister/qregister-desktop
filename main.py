import os
import random
import calendar
import time
import pyqrcode
import tkinter as tk
import uuid
from PIL import Image, ImageTk
from firebase.setup import send_data, firebase_init, update_stores
from helpers.core import generate_sample_receipt, generate_hash, convert_receipt_to_firebase, convert_stores_to_list, \
    currency_symbol

# Detect first time
first = True


def activate_generate_button() -> None:
    """
    Activate "Generate" button

    :return: None
    """

    button_generate['state'] = 'normal'


def close() -> None:
    """
    Exit from app

    :return: None
    """

    window.destroy()





