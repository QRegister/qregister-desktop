import argparse
import os

# Disabling Kivy arguments
os.environ["KIVY_NO_ARGS"] = "1"

from gui.core import run

# Parser Settings
parser = argparse.ArgumentParser(description='Welcome to QRegister!')
parser.add_argument('-f', '--fill_inventory', dest='inventory', action='store_true', help='fill inventory values')
parser.add_argument('-r', '--raspberry', dest='raspberry', action='store_true', help='set ui for raspberry pi')
parser.add_argument('-s', '--full_screen', dest='full_screen', action='store_true', help='run app on full screen')
parser.add_argument('-u', '--update', dest='update', action='store_true', help='update store data before running')
parser.add_argument('-n', '--not_execute', dest='not_execute', action='store_true', help='do not run app')

# Setting Default values
parser.set_defaults(inventory=False, raspberry=False, full_screen=False, update=False, not_execute=False)

args = parser.parse_args()

# Run Kivy app
run(update_store=args.update,
    is_raspberry_pi=args.raspberry,
    is_full_screen=args.full_screen,
    inventory=args.inventory,
    not_execute=args.not_execute)
