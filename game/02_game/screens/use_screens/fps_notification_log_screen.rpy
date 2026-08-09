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
                color "#fff"
                align 0.5, 0.5