screen fps_game_over_screen(debug_mode=False): ## TODO: This screen should probably take some parameters that define what the buttons do
   
    fixed:
        xysize 1.0, 1.0

        add Solid("#800") at t_fps_fade_from_clear(0.5, 0.5)

        text "You died!":
            font "images/fps/ui/fonts/fps_font.ttf"
            size 120
            align 0.5, 0.5
            color "#800"
            outlines [(2, "#fff", 0, 0)]

        hbox:
            align 0.5, 0.65

            use fps_button_screen(
                (200, 100),
                text="Retry",
                on_click=[Function(fps_fader.fade_out_jump_in, "start_game")]
            )

            null width 100

            use fps_button_screen(
                (200, 100),
                text="Quit",
                on_click=[MainMenu(False, False)] ## TODO: this is a temporary solution. Should probably not boot us to main menu in a real game
            )