from PyQt5.QtGui import QColor


def colour_from_hex(hex):
    colour = QColor()
    colour.setNamedColor(hex)
    return colour


class Colours:
    orange = colour_from_hex("#f3a712")
    dark_grey = colour_from_hex("#2d2f3a")
    light_grey = colour_from_hex("#4d5061")
    green = colour_from_hex("#63a46c")
    red = colour_from_hex("#e4572e")
    white = colour_from_hex("#ffffff")