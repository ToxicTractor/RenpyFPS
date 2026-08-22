import renpy
from renpy.display.transform import Transform
from renpy.display.im import Image
from renpy.display.layout import Composite
from game.code.fps.classes.GameEvent_ren import GameEvent
from game.code.fps.classes.settings.FpsConstants_ren import FpsConstants
from game.code.fps.classes.settings.FpsSettings_ren import FpsSettings
from game.code.fps.classes.world.cells.CellBase_ren import CellBase
from game.code.fps.enums.ECellType_ren import ECellType
from game.code.fps.enums.EDirection_ren import EDirection
from game.code.fps.enums.ENotificationType_ren import ENotificationType

"""renpy
init python:
"""

class ButtonCell(CellBase):
    def __init__(self, 
        coord:                      tuple, ## int, int 
        wall_images:                dict, ## single Image or dict (EDirection, Image)
        on_images:                  dict, ## single Image or dict (EDirection, Image)
        off_images:                 dict, ## single Image or dict (EDirection, Image)
        sides:                      list, ## list of EDirections
        on_audio:                   str=None,
        off_audio:                  str=None,
        unlock_audio:               str=None,
        locked_audio:               str=None,
        is_on:                      bool=False, 
        mirrored:                   bool=False,             
        can_be_closed:              bool=True,
        is_locked:                  bool=False, 
        unlocked_by_item:           str=None,
        consumed_on_unlock_count:   int=0,
        locked_notification:        str=FpsConstants.LOCKED_BUTTON_NOTIFICATION):
        super().__init__(coord)

        self.type = ECellType.Button
        self.sides = sides
        self.is_on = is_on
        self.mirrored = mirrored
        self.button_event = GameEvent()

        self.can_be_closed = can_be_closed
        self.is_locked = is_locked
        self.unlocked_by_item = unlocked_by_item
        self.consumed_on_unlock_count = consumed_on_unlock_count
        self.locked_notification = locked_notification

        self.on_audio = on_audio #"audio/fps/map/buttons/turn_on_switch.ogg"
        self.off_audio = off_audio #"audio/fps/map/buttons/turn_off_switch.ogg"
        self.unlock_audio = unlock_audio
        self.locked_audio = locked_audio

        self._wall_images = self._construct_wall_images_dict(wall_images)
        self._on_images = self._construct_overlay_images_dict(on_images)
        self._off_images = self._construct_overlay_images_dict(off_images)

    @property
    def overlay_image(self):
        return self._on_image if self.is_on else self._off_image


    def _construct_wall_images_dict(self, wall_images):
        if (isinstance(wall_images, dict)):
            return wall_images
        else:
            return {key:wall_images for key in (FpsConstants.DIRECTIONS)}


    def _construct_overlay_images_dict(self, images):
        new_dict = {}
        if (images is None):
            return new_dict

        if (not isinstance(images, dict)):
            images = {key:images for key in (FpsConstants.DIRECTIONS)}

        for side, wall_image in self._wall_images.items():

            if (side not in images):
                continue

            overlay_image = self._apply_image_flip(images[side], side)

            new_dict[side] = Composite(
                (FpsSettings.TEXTURE_SIZE, FpsSettings.TEXTURE_SIZE),
                (0, 0), wall_image,
                (0, 0), overlay_image)

        return new_dict


    def _apply_image_flip(self, image, direction):

        if ((direction in (EDirection.Right, EDirection.Up) and not self.mirrored) or
            (direction in (EDirection.Left, EDirection.Down) and self.mirrored)):
            return Transform(image, xzoom=-1.0)
        else:
            return image


    def get_texture(self, side):

        if (side in self.sides):
            return (self._on_images.get(side) if self.is_on else self._off_images.get(side)), 1.0
        else:
            return self._wall_images.get(side), 1.0


    def is_interactable(self, side):

        if (side is None):
            return False

        if (not self.can_be_closed and self.is_on):
            return False

        return side in self.sides


    def interact(self, game):

        if (not self._try_unlock(game)):
            return

        self.is_on = not self.is_on

        renpy.play(self.on_audio if self.is_on else self.off_audio)

        self.button_event.invoke()


    def is_button_side(self, hit_direction):

        if (self.sides is None):
            return False

        return hit_direction in self.sides


    def _try_unlock(self, game) -> bool: ## returns true if the button was not locked or was unlocked

        ## if the buton wasnt locked, we just return true
        if (not self.is_locked):
            return True

        ## if the button is not unlocked by an item, we cant use it so we show a generic notification
        if (self.unlocked_by_item is None):

            if (self.locked_audio):
                renpy.play(self.locked_audio)

            game.notification.show(self.locked_notification, type=ENotificationType.Negative)
            return False

        ## ------------------------------
        ## button consumes item on unlock
        ## ------------------------------
        if (self.consumed_on_unlock_count > 0):

            ## if the player has enough of the required item we unlock the button and remove the items from the player inventory
            if (game.player.inventory.has_item(self.unlocked_by_item, self.consumed_on_unlock_count)):
                self.is_locked = False

                if (self.unlock_audio):
                    renpy.play(self.unlock_audio)

                game.player.inventory.remove_item(self.unlocked_by_item, self.consumed_on_unlock_count)
                game.notification.show(f"{self.consumed_on_unlock_count} x {self.unlocked_by_item.name} was removed.")

                return True

            ## if the player doesn't have enough of the required item we just show a notification
            if (self.locked_audio):
                renpy.play(self.locked_audio)

            game.notification.show(f"Requires {self.consumed_on_unlock_count} x {self.unlocked_by_item.name}.", type=ENotificationType.Negative)
            return False

        ## -------------------------------------
        ## button doesn't consume item on unlock
        ## -------------------------------------

        ## if the player has the item we unlock the button
        if (game.player.inventory.has_item(self.unlocked_by_item)):
            self.is_locked = False

            if (self.unlock_audio):
                renpy.play(self.unlock_audio)

            return True

        ## if the player doesn't have the item we show a notification
        if (self.locked_audio):
            renpy.play(self.locked_audio)

        game.notification.show(f"Requires {self.unlocked_by_item.name}.", type=ENotificationType.Negative)

        return False
