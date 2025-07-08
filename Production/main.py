# Neya's Hackpad code
import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import MatrixScanner
from kmk.keys import KC
from kmk.extensions.encoder import Encoder
from kmk.modules.macros import Macros
from kmk.extensions.peg_oled_display import Oled, OledDisplayMode, OledReactionType
from kmk.extensions.rgb import RGB
from kmk.modules.macros import Press, Release
import time
import random


keyboard = KMKKeyboard()
macros = Macros()
keyboard.modules.append(macros)


class RandomRGB:
    def __init__(self, rgb_extension, interval=0.25):
        self.rgb = rgb_extension
        self.interval = interval
        self.last_update = time.monotonic()

    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        now = time.monotonic()
        if now - self.last_update > self.interval:
            for i in range(self.rgb.num_pixels):
                # Generate random HSV values
                h = random.randint(0, 255)
                s = 255
                v = 128
                self.rgb.set_hsv(i, h, s, v)
            self.last_update = now


rgb = RGB(pixel_pin=board.D1, num_pixels=2)
keyboard.extensions.append(rgb)
keyboard.extensions.append(RandomRGB(rgb))


shrug = KC.MACRO("¯\\_(ツ)_/¯")
nospace = KC.MACRO("​")
react = KC.MACRO(
    Press(KC.LCMD),
    Press(KC.LSFT),
    Press(KC.BSLS),
    Release(KC.BSLS),
    Release(KC.LSFT),
    Release(KC.LCMD)
)

# key matrix
ROW_PINS = (board.D11, board.D10, board.D9)
COL_PINS = (board.D8, board.D7, board.D4)
keyboard.matrix = MatrixScanner(
    row_pins=ROW_PINS,
    col_pins=COL_PINS,
    diode_orientation=MatrixScanner.DIODE_COL2ROW,
)

keyboard.keymap = [
    [KC.RGHT, nospace, react,
     KC.LEFT, KC.DOWN, KC.F9,
     KC.F8, KC.UP, shrug],  # F8 is rotary encoder button
]

# Rotary encoder
encoder = Encoder(
    pins=((board.D2, board.D3),),
    map=[
        ((KC.VOLU,), (KC.VOLD,)),  # CW, CCW
    ]
)
keyboard.extensions.append(encoder)

# OLED
oled_ext = Oled(
    width=128,
    height=32,
    to_display=OledDisplayMode.LAYER,
    flip=False,
    i2c_addr=0x3C,
    reactions=[
        OledReactionType.KEYPRESS,
        OledReactionType.LAYER_CHANGE,
    ],
)
keyboard.extensions.append(oled_ext)

if __name__ == '__main__':
    keyboard.go()
