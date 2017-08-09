from PyQt5.QtGui import QColor


def colour_from_hex(hex: str) -> QColor:
    colour = QColor()
    colour.setNamedColor(hex)
    return colour


class Colours:
    orange: QColor = colour_from_hex("#f3a712")
    dark_grey: QColor = colour_from_hex("#2d2f3a")
    light_grey: QColor = colour_from_hex("#4d5061")
    green: QColor = colour_from_hex("#63a46c")
    red: QColor = colour_from_hex("#e4572e")
    white: QColor = colour_from_hex("#ffffff")
