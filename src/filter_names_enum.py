from enum import Enum


class FilterNamesEnum(Enum):
    """
    IMPORTANT ai filters name should start with "ai_"
    """
    AI_CANDY = "Candy"
    AI_FEATHERS = "Feathers"
    AI_MOSAIC = "Mosaic"
    AI_STARRY_NIGHT = "Starry night"
    AI_WAVE = "Wave"
    
    GREYSCALE = "Черно-белое"
    BROWN = "Сепия"
    INVERT = "Инвертирование"
    HAND_DRAWN = "Рисунок"
    EMBOSS = "Рельеф"
