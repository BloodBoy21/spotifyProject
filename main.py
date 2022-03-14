import lcd as LCD
import spotify as SP
import _thread as thread
from time import *

player = SP.initialize()

mylcd = LCD.lcd()


def print_track(track):
    trackInfo = track.split("\n")
    mylcd.lcd_clear()
    mylcd.lcd_display_string(trackInfo[0], 1, 0)
    mylcd.lcd_display_string(trackInfo[1], 2, 0)


def main():
    SP.run(player, print_track)
