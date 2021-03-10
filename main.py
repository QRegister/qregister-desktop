import argparse
import os

# Disabling Kivy arguments
os.environ["KIVY_NO_ARGS"] = "1"

from gui.core import run

# Parser Settings
parser = argparse.ArgumentParser(description='Welcome to QRegister!')
parser.add_argument('--full_screen', dest='full_screen', action='store_true', help='Run app on full screen')
parser.add_argument('--raspberry', dest='raspberry', action='store_true', help='Run app on Raspberry')
parser.add_argument('--update', dest='update', action='store_true', help='Update store data before running')
parser.set_defaults(raspberry=False, update=False, full=False)

args = parser.parse_args()

# Run Kivy app
run(store_update=args.update, is_raspberry_pi=args.raspberry, is_full_screen=args.full_screen)
