screen FpsScreen():

    modal True

    default fps = FpsDisplayable(scale=30)
    default fps_fader = FpsFadeOverlay(fps)
    default fps_ui = FpsUIOverlay(fps)

    add fps
    add fps_ui

    fixed: ## UI BLOCK 1
        pos 6, 818
        xysize 814, 256
        # add Solid("#0ff")
        # text "BLOCK 1":
        #     font "images/fps/ui/fonts/fps_font.ttf"
        #     color "000"
        #     align 0.5, 0.5

        fixed: ## HEALTH
            align 0.5, 0.5
            xysize 200, 100
            # add Solid("#0ff")

            text f"{fps.player.health}%":
                font "images/fps/ui/fonts/fps_font.ttf"
                size 80
                align 0.5, 0.0
                text_align 0.5
                color "#800"
                outlines [(2, "fff", 0, 0)]
            text "HEALTH":
                font "images/fps/ui/fonts/fps_font.ttf"
                size 40
                align 0.5, 1.0
                color "#999"

    fixed: ## UI FACE BLOCK
        pos 832, 818
        xysize 256, 256
        # add Solid("#f0f")
        # text "FACE":
        #     font "images/fps/ui/fonts/fps_font.ttf"
        #     color "fff"
        #     align 0.5, 0.5

    fixed: ## UI BLOCK 2
        pos 1100, 818
        xysize 814, 256
        # add Solid("#ff0")
        # text "BLOCK 2":
        #     font "images/fps/ui/fonts/fps_font.ttf"
        #     color "000"
        #     align 0.5, 0.5
    
    if (fps.show_framerate):
        fixed: ## FRAME RATE COUNTER
            align 0.996, 0.995
            xysize 140, 60
            #add Solid("#f0f")
            vbox:
                hbox:
                    spacing 10
                    text "FPS:":
                        align 0.0, 0.5
                        font "images/fps/ui/fonts/fps_font.ttf"
                        color "#fff"
                    text f"{fps.framerate}":
                        align 0.0, 0.5
                        font "images/fps/ui/fonts/fps_font.ttf"
                        color "#fff"
                    
                hbox:
                    spacing 10
                    text "AVG:":
                        align 0.0, 0.5
                        font "images/fps/ui/fonts/fps_font.ttf"
                        color "#fff"
                    text f"{fps.framerate_avg}":
                        align 0.0, 0.5
                        font "images/fps/ui/fonts/fps_font.ttf"
                        color "#fff"
    
    if (not fps.player.is_alive):
        
        fixed:
            align 0.5, 0.5
            xysize 1.0, 1.0
            add Solid("#800") at t_fps_fade_from_clear(0.5, 0.5)
            text "You died. Retry?":
                font "images/fps/ui/fonts/fps_font.ttf"
                size 120
                align 0.5, 0.5
                color "#800"
                outlines [(2, "fff", 0, 0)]

    add fps_fader

