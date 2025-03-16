import numpy as np


bounds = (np.array([[219, 418], [679, 276], [1231, 515], [729, 966], [429, 979]], np.int32), (15, 245, 76))
lines = {
        "to-left-delimiter": ((259, 527), (759, 309), (241, 130, 32)),
        "to-right-delimiter": ((362, 797), (960, 396), (241, 130, 32)),
        "left-right-delimiter": ((301, 636), (847, 350), (235, 28, 28)),
        "to-bottom-delimiter": ((375, 371), (580, 493), (37, 195, 223)),
        "to-top-delimiter": ((679, 441), (1085, 646), (37, 195, 223)),
        "bottom-top-delimiter-left": ((580, 493), (1006, 717), (21, 63, 231)),
        "bottom-top-delimiter-right": ((492, 336), (679, 441), (21, 63, 231)),
    }