screen fps_notification_log_screen(debug_mode=False):
    
    fixed:
        pos 0, 700
        xysize 1.0, 0.1

        if (debug_mode):
            add Solid("#f0f")
            text "LOG":
                color "#fff"
                align 0.5, 0.5

        if (fps.notification.is_active):            
            text fps.notification.text:
                color  FpsSettings.NOTIFICATION_COLORS.get(fps.notification.type, FpsSettings.DEFAULT_NOTIFICATION_COLOR)
                outlines FpsSettings.NOTIFICATION_OUTLINES.get(fps.notification.type, FpsSettings.DEFAULT_NOTIFICATION_OUTLINES)
                align 0.5, 0.5