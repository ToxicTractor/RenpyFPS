screen fps_ui_screen(fps):
    style_prefix "fps"

    $ debug_mode = False

    #region Force screen update
    ## Hacky way to force update screen at 20 FPS
    ## Setting the frame rate to high will break hover/unhover events on buttons
    default screen_lifetime = 0
    timer 0.05 repeat True action IncrementLocalVariable("screen_lifetime", 1)
    #endregion

    add "fps_ui_base":
        yalign 1.0

    add "fps_crosshair" at t_fps_tint(FpsSettings.CROSSHAIR_COLOR), t_fps_alpha(FpsSettings.CROSSHAIR_ALPHA):
        xalign 0.5
        yanchor 0.5
        ypos FpsSettings.RAW_HALF_SCREEN_HEIGHT

    fixed: ## NOTIFICATIONS BLOCK
        use fps_notification_log_screen(
            debug_mode = debug_mode
        )

    $ block_width   = 814
    $ block_height  = 256

    fixed: ## UI BLOCK LEFT
        pos 6, 818
        xysize 814, 256

        if (debug_mode):
            add Solid("#0ff")
            text "BLOCK LEFT":
                color "#000"
                align 0.5, 0.5

        $ title_height = 48
        $ weapon_size = 64
        $ numbers_height = 32

        use fps_weapons_screen(
            fps,
            title_height,
            weapon_size,
            numbers_height,
            debug_mode = debug_mode
        )

        use fps_resource_screen(
            fps,
            height              = block_height - (title_height + weapon_size + numbers_height),
            ammo_color          = "#a77500",
            health_color        = "#800",
            armor_color         = "#004d88",
            resource_name_color = "#999",
            debug_mode          = debug_mode
        )

    fixed: ## UI FACE BLOCK
        pos 832, 818
        xysize 256, 256

        if (debug_mode):    
            add Solid("#f0f")
            text "FACE":
                color "#fff"
                align 0.5, 0.5

        add fps.player.face.get_image()

    $ block_width   = 814
    $ block_height  = 256


    fixed: ## UI BLOCK RIGHT
        pos 1100, 818
        xysize block_width, block_height
        
        if (debug_mode):
            add Solid("#ff0")
            text "BLOCK RIGHT":
                color "#000"
                align 0.5, 0.5

        $ left_margin   = 12
        $ title_height  = 32
        $ item_size     = 64
        $ items_per_row = 12
        $ row_count     = 2
        $ item_spacing  = 2

        use fps_inventory_screen(
            left_margin,
            title_height,
            item_size,
            items_per_row,
            row_count,
            item_spacing,
            debug_mode
        )

        $ inventory_height = title_height + row_count * item_size + (row_count - 1) * item_spacing

        fixed:
            ypos inventory_height
            xysize 1.0, block_height - inventory_height
            
            if (debug_mode):
                add Solid("#f0f")

            ## pause menu button
            use fps_button_screen(
                xysize              = (256, 64), 
                align               = (0.5, 0.5), 
                text                = "Menu", 
                text_offset         = (0, -3),
                sensitive           = fps.player.is_alive,
                tint_on_insensitive = False
            )
            
    
    if (fps.show_framerate):
        use fps_framerate_screen(
            align = (0.996, 0.995),
            debug_mode = debug_mode
        )

    if (fps.is_won):
        use fps_victory_screen(
            debug_mode = debug_mode
        )

    if (not fps.player.is_alive):
        use fps_game_over_screen(
            debug_mode = debug_mode
        )