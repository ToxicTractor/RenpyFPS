screen fps_weapons_screen(
    fps, 
    title_height, 
    weapon_size, 
    numbers_height, 
    debug_mode=False):
    
    $ left_margin = 15
    $ weapons = fps.player.weapons
    $ max_weapon_count = 10
    $ space = 16

    $ current_weapon_name = "None" if fps.player.equipped_weapon is None else fps.player.equipped_weapon.name

    fixed:
        xysize 1.0, title_height + weapon_size + numbers_height
        if (debug_mode):
            add Solid("#0f0")

        fixed:
            xysize 1.0, title_height

            hbox:
                xpos left_margin
                yalign 0.5

                text "CURRENT WEAPON:":
                    yalign 0.5

                text f" {current_weapon_name}":
                    yalign 0.5

        for i, weapon in enumerate(weapons):
            
            ## we can only display a certain amount of weapons
            if (i >= max_weapon_count):
                break

            fixed:
                pos left_margin + i * weapon_size + space * i, title_height
                xysize weapon_size, weapon_size
                
                if (weapons[i].icon):
                    add weapons[i].icon:
                        align 0.5, 0.5

                else:
                    add Solid("#f0f") ## if weapon has no icon we display pink to flag it clearly

                if fps.player.equipped_weapon_index == i:
                    add Frame("images/fps/ui/frame.png", 12, 12) at t_fps_tint("#ffc144")

                else:
                    add Frame("images/fps/ui/frame.png", 12, 12)
            
            fixed:
                pos left_margin + i * weapon_size + space * i, weapon_size + title_height
                xysize weapon_size, numbers_height

                text f"{i + 1 if i != 9 else 0}":
                    align 0.5, 0.5