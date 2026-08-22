from game.code.fps.classes.AnimationData_ren import AnimationData

"""renpy
init -9 python:
"""

class FpsAnimations():

    #region Static objects

    candlestick = AnimationData("candlestick", None)
    torch = AnimationData("torch_animated", 0.4, True)

    #endregion

    #region Pickups

    red_keycard_pickup = AnimationData("red_keycard", None)
    red_key_pickup = AnimationData("red_key", None)
    yellow_keycard_pickup = AnimationData("yellow_keycard", None)
    yellow_key_pickup = AnimationData("yellow_key", None)
    blue_keycard_pickup = AnimationData("blue_keycard", None)
    blue_key_pickup = AnimationData("blue_key", None)

    #endregion
