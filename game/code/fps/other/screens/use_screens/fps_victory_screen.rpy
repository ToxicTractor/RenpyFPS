screen fps_victory_screen(debug_mode=False): ## TODO: This screen should probably take some parameters that define what the button do
    
    fixed:
        xysize 1.0, 1.0

        add Solid("#111f") at t_fps_fade_from_clear(0.5, 0.5)

        text "You won! Here have a cookie!":
            font "images/fps/ui/fonts/fps_font.ttf"
            size 80
            align 0.5, 0.5
            color "#fff"
            outlines [(2, "#111", 0, 0)]

        add "cookie":
            align 0.5, 0.25
            zoom 0.25

        use fps_button_screen(
            (200, 100),
            align=(0.5, 0.65),
            text="Yay!",
            on_click=[MainMenu(False, False)] ## TODO: this is a temporary solution. Should probably not boot us to main menu in a real game
            ) 