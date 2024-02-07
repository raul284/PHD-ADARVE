from enum import Enum

class UserInputType(Enum):
    DEFAULT = 0
    IA_MOVE_LEFT = 1
    IA_MOVE_RIGHT = 2
    IA_MENU_INTERACT_LEFT = 3
    IA_MENU_INTERACT_RIGHT = 4
    IA_GRAB_LEFT = 5
    IA_GRAB_RIGHT = 6