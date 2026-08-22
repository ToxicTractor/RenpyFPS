from game.code.fps.enums.EEmotion_ren import EFaceEmote
from renpy.display.im import Image
from renpy.display.image import ImageReference

"""renpy
init -100 python:
"""

class FpsTextures():

    WALLS = {
        1: Image("images/fps/textures/walls/stone_wall_01.jpg", oversample=4),
        2: Image("images/fps/textures/walls/stone_wall_02.png", oversample=1.875),
        3: Image("images/fps/textures/walls/stone_wall_03.png", oversample=1.875),
        4: Image("images/fps/textures/walls/stone_wall_04.png", oversample=1.875),
        5: Image("images/fps/textures/walls/wood_wall_01.png", oversample=1.875),
        6: Image("images/fps/textures/walls/stone_wall_05.png", oversample=1.875),
    }

    WALL_OVERLAYS = {
        0: Image("images/fps/textures/walls/overlays/get_a_job.png")
    }

    DOORS = {
        0: Image("images/fps/textures/doors/metal_door.png", oversample=0.25),
        1: Image("images/fps/textures/doors/blue_door.png", oversample=0.25),
        1000: Image("images/fps/textures/doors/door_slim_side.png", oversample=0.25)
    }

    BUTTONS = {
        0: Image("images/fps/textures/buttons/switch_01_on.png"),
        1: Image("images/fps/textures/buttons/switch_01_off.png"),
        2: Image("images/fps/textures/buttons/blue_keycard_reader_on.png"),
        3: Image("images/fps/textures/buttons/blue_keycard_reader_off.png"),
        4: Image("images/fps/textures/buttons/red_keycard_reader_on.png"),
        5: Image("images/fps/textures/buttons/red_keycard_reader_off.png"),
        6: Image("images/fps/textures/buttons/yellow_keycard_reader_on.png"),
        7: Image("images/fps/textures/buttons/yellow_keycard_reader_off.png"),
    }

    FACES = {
        EFaceEmote.Neutral: [
            ImageReference("fps_face_20_neutral"),
            ImageReference("fps_face_40_neutral"),
            ImageReference("fps_face_60_neutral"),
            ImageReference("fps_face_80_neutral"),
            ImageReference("fps_face_100_neutral"),
        ],
        EFaceEmote.Crazed: [
            ImageReference("fps_face_20_crazed"),
            ImageReference("fps_face_40_crazed"),
            ImageReference("fps_face_60_crazed"),
            ImageReference("fps_face_80_crazed"),
            ImageReference("fps_face_100_crazed"),
        ],
        EFaceEmote.Hurt: [
            ImageReference("fps_face_20_hurt"),
            ImageReference("fps_face_40_hurt"),
            ImageReference("fps_face_60_hurt"),
            ImageReference("fps_face_80_hurt"),
            ImageReference("fps_face_100_hurt"),
        ],
        EFaceEmote.LookLeft: [
            ImageReference("fps_face_20_left"),
            ImageReference("fps_face_40_left"),
            ImageReference("fps_face_60_left"),
            ImageReference("fps_face_80_left"),
            ImageReference("fps_face_100_left"),
        ],
        EFaceEmote.LookRight: [
            ImageReference("fps_face_20_right"),
            ImageReference("fps_face_40_right"),
            ImageReference("fps_face_60_right"),
            ImageReference("fps_face_80_right"),
            ImageReference("fps_face_100_right"),
        ]
    }