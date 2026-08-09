screen fps_button_screen(
    xysize, 
    pos=None, 
    anchor=None,
    align=None,
    text=None,
    text_offset=(0, 0),
    text_color="#fff",
    text_size=None,
    text_outlines=[(2, "#111", 0, 0)],
    sensitive=True,
    tint_on_insensitive=True,
    on_click=None, 
    on_hover=[], 
    on_unhover=[]):

    $ insensitive_tint = "#0008"
    default is_hovered = False

    fixed:
        xysize xysize
        
        ## set pos and anchor if given
        if (pos):
            pos pos
        if (anchor):
            anchor anchor

        ## then set align if given
        ## align take priority over pos and anchor
        if (align):
            align align

        button:
            xysize 1.0, 1.0
            padding (0, 0)
            
            action (NullAction() if on_click is None else on_click)

            hovered [SetLocalVariable("is_hovered", True)] + on_hover
            unhovered [SetLocalVariable("is_hovered", False)] + on_unhover

            sensitive sensitive

            fixed:
                if (sensitive or not tint_on_insensitive):
                    if (is_hovered):
                        add Frame("images/fps/ui/button_hover.png", 6, 6)
                    else:
                        add Frame("images/fps/ui/button_idle.png", 6, 6)
                else:
                    add Frame("images/fps/ui/button_idle.png", 6, 6) at t_fps_tint(insensitive_tint)

                if (text is not None):
                    if (sensitive or not tint_on_insensitive):
                        text text:
                            align 0.5, 0.5
                            offset text_offset

                            if (text_color is not None):
                                color text_color
                            
                            if (text_size is not None):
                                size text_size
                            
                            if (text_outlines is not None):
                                outlines text_outlines
                    else:
                        text text at t_fps_tint(insensitive_tint):
                            align 0.5, 0.5
                            offset text_offset

                            if (text_color is not None):
                                color text_color
                            
                            if (text_size is not None):
                                size text_size
                            
                            if (text_outlines is not None):
                                outlines text_outlines
