import numpy as np

# RGB -> BGR
polygons = {
        "frame": (np.array([[219, 418], [679, 276], [1231, 515], [729, 966], [429, 979]], np.int32), (15, 245, 76)),
        "to-right-check": (np.array([[0, 897], [164, 767], [256, 1048], [182, 1080], [0, 1080]], np.int32), (255, 35, 211)),
        "to-bottom-check": (np.array([[288, 369], [270, 340], [393, 307], [421, 329]], np.int32), (255, 35, 211)),
        "to-left-check": (np.array([[773, 274], [821, 258], [940, 277], [854, 305]], np.int32), (255, 35, 211)),
        "to-top-check": (np.array([[1162, 809], [1277, 650], [1446, 738], [1329, 900]], np.int32), (255, 35, 211)),
          }
lines = {
        "to-left-delimiter": ((259, 527), (759, 309), (32, 130, 241)),
        "to-right-delimiter": ((362, 797), (960, 396), (32, 130, 241)),
        "left-right-delimiter": ((301, 636), (847, 350), (28, 28, 235)),
        "to-bottom-delimiter": ((375, 371), (580, 493), (223, 195, 37)),
        "to-top-delimiter": ((679, 441), (1085, 646), (223, 195, 37)),
        "bottom-top-delimiter-left": ((580, 493), (1006, 717), (231, 63, 21)),
        "bottom-top-delimiter-right": ((492, 336), (679, 441), (231, 63, 21)),
    }
lanes = {
        "to-left": (np.array([[219, 418], [680, 275], [847, 350], [301, 636]], np.int32), (28, 28, 235)),
        "to-left-right-lane": (np.array([[219, 418], [680, 275], [758, 309], [259, 526]], np.int32), (32, 130, 241)),
        "to-left-left-lane": (np.array([[259, 526], [758, 309], [847, 350], [301, 636]], np.int32), (32, 130, 241)),
        "to-right": (np.array([[301, 636], [847, 350], [1231, 515], [730, 966], [429, 979]], np.int32), (28, 28, 235)),
        "to-right-right-lane": (np.array([[362, 797], [957, 396], [1231, 515], [730, 966], [429, 979]], np.int32), (32, 130, 241)),
        "to-right-left-lane": (np.array([[301, 636], [847, 350], [958, 397], [361, 797]], np.int32), (32, 130, 241)),
        "to-bottom": (np.array([[219, 418], [492, 333], [677, 439], [578, 491], [1007, 717], [729, 966], [429, 979]], np.int32), (231, 63, 21)),
        "to-bottom-right-lane": (np.array([[219, 418], [375, 370], [1007, 717], [729, 966], [429, 979]], np.int32), (223, 195, 37)),
        "to-bottom-left-lane": (np.array([[375, 370], [492, 333], [677, 439], [578, 491]], np.int32), (223, 195, 37)),
        "to-top": (np.array([[492, 333], [679, 276], [1231, 515], [1007, 717], [578, 491], [677, 439]], np.int32), (231, 63, 21)),
        "to-top-right-lane": (np.array([[492, 333], [679, 276], [1231, 515], [1086, 646]], np.int32), (223, 195, 37)),
        "to-top-left-lane": (np.array([[578, 491], [677, 439], [1086, 646], [1007, 717]], np.int32), (223, 195, 37))
}
