screen fps_resource_screen(
    fps, 
    height              = 1.0, 
    ammo_color          = "#000", 
    health_color        = "#000", 
    armor_color         = "#000", 
    resource_name_color = "#000", 
    outlines            = [(2, "#fff", 0, 0)], 
    debug_mode          = False):
    
    fixed:
        align 1.0, 1.0
        xysize 1.0, height
        
        #region Health and Armor

        fixed:
            xalign 1.0
            xysize 0.5, 1.0

            if (debug_mode):
                add Solid("#f00")

            fixed: ## HEALTH
                align 0.0, 0.5
                xysize 0.5, 1.0

                if (debug_mode):
                    add Solid("#0ff")
                
                text f"{fps.player.health}%":
                    size 80
                    align 0.5, 0.0
                    text_align 0.5
                    color health_color
                    outlines outlines
                text "HEALTH":
                    size 40
                    align 0.5, 1.0
                    color resource_name_color
            
            fixed: ## ARMOR
                align 1.0, 0.5
                xysize 0.5, 1.0

                if (debug_mode):
                    add Solid("#0ff")
                
                text f"{fps.player.armor}%":
                    size 80
                    align 0.5, 0.0
                    text_align 0.5
                    color armor_color
                    outlines outlines
                text "ARMOR":
                    size 40
                    align 0.5, 1.0
                    color resource_name_color

        #endregion

        #region Ammo

        fixed:
            xalign 0.0
            xysize 0.5, 1.0

            if (debug_mode):
                add Solid("#00f")

            fixed: ## AMMO
                align 0.5, 0.5
                xysize 1.0, 1.0
                
                text f"{fps.player.equipped_weapon.formatted_ammo}":
                    size 80
                    align 0.5, 0.0
                    text_align 0.5
                    color ammo_color
                    outlines outlines

                text "AMMO":
                    size 40
                    align 0.5, 1.0
                    color resource_name_color

        #endregion