
import cv2
import numpy as np
import time

from src.video_capture import get_cap

def main():
    cap = get_cap() # Инициализация захвата видео

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

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.polylines(frame, [bounds[0]], isClosed=True, color=bounds[1], thickness=2) # Устанавливаем границу
        for line in lines.values():
            start_point, end_point, color = line
            thickness = 2
            cv2.line(frame, start_point, end_point, color, thickness)

        # Вывод изображения
        cv2.imshow("Traffic Monitoring", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

    # Завершение работы
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()