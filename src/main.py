
import cv2
import time

from capture import get_cap
from markup import bounds, lines

def main():
    cap = get_cap() # Инициализация захвата видео

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