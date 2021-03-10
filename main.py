import argparse
import os

from gui.core import run

os.environ["KIVY_NO_ARGS"] = "1"

parser = argparse.ArgumentParser(description='Welcome to QRegister')

parser.add_argument('--raspberry', dest='raspberry', action='store_true')
parser.add_argument('--no-raspberry', dest='raspberry', action='store_false')

parser.add_argument('--update', dest='update', action='store_true')
parser.add_argument('--no--update', dest='update', action='store_true')

parser.set_defaults(raspberry=False, update=False)

args = parser.parse_args()

run(store_update=args.update, is_raspberry_pi=args.raspberry)
