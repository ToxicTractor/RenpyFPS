default fps_fader = FpsFadeOverlay()

label start:

    label game_setup:
    $ quick_menu = False
    show screen fps_fade_screen()

    label start_game:
    show screen fps_screen()

    pause

    return
