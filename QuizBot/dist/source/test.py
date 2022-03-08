from time import *
import random
from ahk import AHK


def beep(time):
    ahk = AHK()

    if bool(1):
        if time == 60:
            ahk.sound_play('beep.mp3')
        elif time == 10:
            ahk.sound_play('source/beep.mp3')
            ahk.sound_play('source/beep.mp3')



beep(60)


