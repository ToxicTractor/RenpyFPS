screen fps_screen():
    modal True
    style_prefix "fps"

    default fps = FpsDisplayable(scale=25)
    default fps_fader = FpsFadeOverlay(fps)
    default fps_ui = FpsUIOverlay(fps)

    add fps
    add fps_ui

    #region ## UI BLOCK LEFT
    fixed: 
        pos 6, 818
        xysize 814, 256
        # add Solid("#0ff")
        # text "BLOCK LEFT":
        #     color "#000"
        #     align 0.5, 0.5

        #region Weapons

        fixed:
            xysize 1.0, 128
            #add Solid("#0f0")
            $ left_space = 15

            fixed:
                xysize 1.0, 32
                hbox:
                    xpos left_space
                    text f"CURRENT WEAPON:":
                        yalign 0.5
                    text f" {fps.player.equipped_weapon.name}":
                        yalign 0.5

            $ weapons = fps.player.weapons
            $ space = 16

            for i in range(10):
                
                fixed:
                    pos left_space + i * 64 + space * i, 32
                    xysize 64, 64
                    add Solid("#111")
                    
                    if (i < len(weapons)):

                        if (weapons[i].icon):
                            add weapons[i].icon:
                                align 0.5, 0.5
                        else:
                            add Solid("#f0f")

                    if fps.player.equipped_weapon_index == i:
                        add Frame("images/fps/ui/frame.png", 12, 12) at t_fps_tint("#ffc144")
                    else:
                        add Frame("images/fps/ui/frame.png", 12, 12)
                
                fixed:
                    pos left_space + i * 64 + space * i, 96
                    xysize 64, 32
                    text f"{i + 1 if i != 9 else 0}":
                        align 0.5, 0.5

        #endregion

        #region Health and Armor

        fixed:
            align 1.0, 1.0
            xysize 0.5, 0.5
            #add Solid("#f00")

            fixed: ## HEALTH
                align 0.0, 0.5
                xysize 200, 100
                #add Solid("#0ff")
                
                text f"{fps.player.health}%":
                    size 80
                    align 0.5, 0.0
                    text_align 0.5
                    color "#800"
                    outlines [(2, "fff", 0, 0)]
                text "HEALTH":
                    size 40
                    align 0.5, 1.0
                    color "#999"
            
            fixed: ## ARMOR
                align 1.0, 0.5
                xysize 200, 100
                #add Solid("#0ff")
                
                text f"{fps.player.armor}%":
                    size 80
                    align 0.5, 0.0
                    text_align 0.5
                    color "#004d88"
                    outlines [(2, "fff", 0, 0)]
                text "ARMOR":
                    size 40
                    align 0.5, 1.0
                    color "#999"

        #endregion

        #region Ammo

        fixed:
            align 0.0, 1.0
            xysize 0.5, 0.5
            #add Solid("#00f")

            fixed: ## AMMO
                align 0.5, 0.5
                xysize 1.0, 100
                
                text f"{fps.player.equipped_weapon.formatted_ammo}":
                    size 80
                    align 0.5, 0.0
                    text_align 0.5
                    color "#a77500"
                    outlines [(2, "fff", 0, 0)]

                text "AMMO":
                    size 40
                    align 0.5, 1.0
                    color "#999"

        #endregion

    #endregion

    fixed: ## UI FACE BLOCK
        pos 832, 818
        xysize 256, 256
        # add Solid("#f0f")
        # text "FACE":
        #     color "fff"
        #     align 0.5, 0.5

    fixed:
        pos 0, 700
        xysize 1.0, 0.1
        # add Solid("#f0f")
        # text "LOG":
        #     color "fff"
        #     align 0.5, 0.5

        if (fps.notification.is_active):
            text fps.notification.text:
                color "fff"
                align 0.5, 0.5

    fixed: ## UI BLOCK RIGHT
        pos 1100, 818
        xysize 814, 256
        # add Solid("#ff0")
        # text "BLOCK RIGHT":
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
    
    if (not fps.player.is_alive):
        
        fixed:
            align 0.5, 0.5
            xysize 1.0, 1.0
            add Solid("#800") at t_fps_fade_from_clear(0.5, 0.5)
            text "You died!":
                font "images/fps/ui/fonts/fps_font.ttf"
                size 120
                align 0.5, 0.5
                color "#800"
                outlines [(2, "fff", 0, 0)]

            hbox:
                align 0.5, 0.65

                button:
                    xysize(200, 100)
                    action Jump("start")
                    fixed:
                        add Solid("#111")
                        add Frame("images/fps/ui/frame.png", 12, 12)
                        text "Retry":
                            align 0.5, 0.5
                
                null width 100

                button:
                    xysize(200, 100)
                    action MainMenu(confirm=False, save=False)
                    fixed:
                        add Solid("#111")
                        add Frame("images/fps/ui/frame.png", 12, 12)
                        text "Quit":
                            align 0.5, 0.5

    add fps_fader

