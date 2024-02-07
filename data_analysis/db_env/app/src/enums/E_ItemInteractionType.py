from enum import Enum

class ItemInteractionType(Enum):
    DEFAULT = 0
    START_DETECTION = 1
    STOP_DETECTION = 2
    GRAB = 3
    RELEASE = 4