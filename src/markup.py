import numpy as np

# RGB -> BGR
bounds = (np.array([[219, 418], [679, 276], [1231, 515], [729, 966], [429, 979]], np.int32), (15, 245, 76))
lines = {
        "to-left-delimiter": ((259, 527), (759, 309), (32, 130, 241)),
        "to-right-delimiter": ((362, 797), (960, 396), (32, 130, 241)),
        "left-right-delimiter": ((301, 636), (847, 350), (28, 28, 235)),
        "to-bottom-delimiter": ((375, 371), (580, 493), (223, 195, 37)),
        "to-top-delimiter": ((679, 441), (1085, 646), (223, 195, 37)),
        "bottom-top-delimiter-left": ((580, 493), (1006, 717), (231, 63, 21)),
        "bottom-top-delimiter-right": ((492, 336), (679, 441), (231, 63, 21)),
    }
