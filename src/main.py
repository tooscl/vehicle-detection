
import cv2
import time

from capture import get_cap
from markup import boxes, lines
from models.yolov8n import yolo8vn
from cls import CLASS_MAP

def main():
    cap = get_cap() # Инициализация захвата видео

    model = yolo8vn # Инициализация модели

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Разметка фрейма
        for box in boxes.values():
            pts, color = box
            thikness = 2
            cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=thikness)
        for line in lines.values():
            start_point, end_point, color = line
            thickness = 2
            cv2.line(frame, start_point, end_point, color=color, thickness=thickness)

        # Определение объектов
        results = model(frame)[0] # Детекции

        # Обход детекций
        for box in results.boxes.data:
            x1, y1, x2, y2, conf, cls = box
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2) # Центр объекта
            cls = int(cls) # Для корректной работы с картой классов
            if cls not in CLASS_MAP: # Не работаем с нецелевыми объектами
                continue


            # # Визуализация боксов
            # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

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