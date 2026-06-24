#region Candlestick
define candlestick_anim = AnimationData("candlestick", 0)
#endregion




#region Torch
define torch_anim = AnimationData("torch_animated", 0.4, True)

image torch_animated = Animation(
    "torch_01", 0.1,
    "torch_02", 0.1,
    "torch_03", 0.1,
    "torch_04", 0.1
) ## 0.4 seconds
#endregion