define config.mouse_hide_time = None

default fps_fader = FpsFadeOverlay()
default fps = None

label start:

    label game_setup:
    $ quick_menu = False
    show screen fps_fade_screen()

    label start_game:
    $ fps = FpsDisplayable(scale=25)
    show screen fps_screen(fps)

    pause

    return
