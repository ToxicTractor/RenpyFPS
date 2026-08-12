transform t_fps_fade_from_clear(amount, duration):
    alpha 0.0
    linear duration alpha amount

transform t_fps_tint(color):
    matrixcolor TintMatrix(color)

transform t_fps_alpha(alpha):
    alpha alpha

transform t_fps_rotate(angle):
    rotate angle