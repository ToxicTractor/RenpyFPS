screen fps_ui_screen(fps):
    modal True
    style_prefix "fps"

    #region Force screen update
    ## Hacky way to force update screen at 20 FPS
    ## Setting the frame rate to high will break hover/unhover events on buttons
    default screen_lifetime = 0
    timer 0.05 repeat True action IncrementLocalVariable("screen_lifetime", 1)
    #endregion

    fixed: ## UI BLOCK LEFT
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

    $ block_width = 814
    $ block_height = 256
    fixed: ## UI BLOCK RIGHT
        pos 1100, 818
        xysize block_width, block_height
        # add Solid("#ff0")
        # text "BLOCK RIGHT":
        #     color "000"
        #     align 0.5, 0.5

        fixed:
            xysize 1.0, 128
            #add Solid("#0f0")
            $ left_space = 12
            $ title_height = 32
            $ item_size = 64

            fixed:
                xysize 1.0, title_height
                text "INVENTORY":
                    align 0.5, 0.5

            $ items_per_row = 12
            $ item_spacing = 2
            $ row_count = 2
            $ shown_items = fps.player.inventory.get_shown_items()
            $ shown_items_count = len(shown_items)

            fixed:
                pos left_space, title_height
                xysize items_per_row * item_size + (items_per_row - 1) * item_spacing, row_count * item_size + (row_count - 1 * item_spacing)
                add Solid("#222")

            grid items_per_row row_count:
                spacing 1
                pos left_space, title_height
                for i in range(items_per_row * row_count):
                    if (i < shown_items_count):
                        $ current_item_count = fps.player.inventory.get_item_count(shown_items[i]) 
                        fixed:
                            xysize item_size, item_size
                            ## TODO: Replace these with buttons so we can add tooltips
                            add shown_items[i].icon:
                                align 0.5, 0.5
                            if (current_item_count > 1):
                                text f"{current_item_count}":
                                    size 24
                                    align 1.0, 1.0
                    else:
                        add Null(item_size, item_size)

        fixed:
            pos left_space, block_height - 64 - 16
            xysize block_width - 2 * left_space, 64
            #add Solid("#f0f")

            ## pause menu button
            use fps_button_screen(
                (300, 1.0), 
                align=(0.5, 0.5), 
                text="Menu", 
                text_offset=(0, -3),
                sensitive=fps.player.is_alive,
                tint_on_insensitive=False
            )
            
    
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
    
    if (fps.is_won):

        fixed:
            align 0.5, 0.5
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
                outlines [(2, "#fff", 0, 0)]

            hbox:
                align 0.5, 0.65

                use fps_button_screen(
                    (200, 100),
                    text="Retry",
                    on_click=[Function(fps_fader.fade_out_jump_in, "start_game")]
                )

                # button:
                #     xysize(200, 100)
                #     action Function(fps_fader.fade_out_jump_in, "start_game")
                #     fixed:
                #         add Solid("#111")
                #         add Frame("images/fps/ui/frame.png", 12, 12)
                #         text "Retry":
                #             align 0.5, 0.5
                
                null width 100

                use fps_button_screen(
                    (200, 100),
                    text="Quit",
                    on_click=[MainMenu(False, False)] ## TODO: this is a temporary solution. Should probably not boot us to main menu in a real game
                )

                # button:
                #     xysize(200, 100)
                #     action MainMenu(confirm=False, save=False) ## TODO: this is a temporary solution. Should probably not boot us to main menu in a real game
                #     fixed:
                #         add Solid("#111")
                #         add Frame("images/fps/ui/frame.png", 12, 12)
                #         text "Quit":
                #             align 0.5, 0.5