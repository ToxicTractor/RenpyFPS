screen fps_framerate_screen(align, debug_mode=False):
    fixed: ## FRAME RATE COUNTER
        align align
        xysize 140, 60

        if (debug_mode):
            add Solid("#0ff")

        vbox:
            ## count is split into 2 to avoid weird jittering when the count changes
            hbox:
                spacing 10
                text "FPS:":
                    align 0.0, 0.5
                    color "#fff"
                text f"{fps.framerate}":
                    align 0.0, 0.5
                    color "#fff"
                
            hbox:
                spacing 10
                text "AVG:":
                    align 0.0, 0.5
                    color "#fff"
                text f"{fps.framerate_avg}":
                    align 0.0, 0.5
                    color "#fff"