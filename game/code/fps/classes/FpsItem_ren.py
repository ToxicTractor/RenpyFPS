from renpy.display.image import ImageReference
from game.code.fps.other.named_tuples_ren import InventoryItem

"""renpy
init python:
"""

class FpsItem():

    ## Keycards
    RED_KEYCARD = InventoryItem("red_keycard", "red keycard", ImageReference("red_keycard_icon"))
    YELLOW_KEYCARD = InventoryItem("yellow_keycard", "yellow keycard", ImageReference("yellow_keycard_icon"))
    BLUE_KEYCARD = InventoryItem("blue_keycard", "blue keycard", ImageReference("blue_keycard_icon"))

    ## Keys
    RED_KEY = InventoryItem("red_key", "red key", ImageReference("red_key_icon"))
    YELLOW_KEY = InventoryItem("yellow_key", "yellow key", ImageReference("yellow_key_icon"))
    BLUE_KEY = InventoryItem("blue_key", "blue key", ImageReference("blue_key_icon"))
