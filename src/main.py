import cv2
import time

from src.video_capture import get_cap

def main():
    cap = get_cap() # Инициализация захвата видео

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Вывод изображения
        cv2.imshow("Traffic Monitoring", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Завершение работы
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()