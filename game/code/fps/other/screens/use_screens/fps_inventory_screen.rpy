screen fps_inventory_screen(
    left_margin, 
    title_height, 
    item_size, 
    items_per_row, 
    row_count, 
    item_spacing, 
    debug_mode=False):
    
    $ shown_items = fps.player.inventory.get_shown_items()
    $ shown_items_count = len(shown_items)
    $ height = title_height + row_count * item_size + (row_count - 1) * item_spacing
     
    fixed:
        xysize 1.0, height

        if (debug_mode):
            add Solid("#f00")

        fixed:
            xysize 1.0, title_height

            text "INVENTORY":
                align 0.5, 0.5

        fixed:
            pos left_margin, title_height
            xysize items_per_row * item_size + (items_per_row - 1) * item_spacing, row_count * item_size + (row_count - 1 * item_spacing)

            add Solid("#222")

        grid items_per_row row_count:
            spacing 1
            pos left_margin, title_height

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