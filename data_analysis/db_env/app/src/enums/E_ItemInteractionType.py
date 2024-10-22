from enum import Enum

class ItemInteractionType(Enum):
    START_DETECTION = 1
    STOP_DETECTION = 2
    GRAB = 3
    RELEASE = 4