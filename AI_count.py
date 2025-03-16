import cv2
import numpy as np
import time
import pandas as pd
from ultralytics import YOLO

from src.video_capture import get_cap


# # === Параметры ===
# VIDEO_SOURCE = "tests/7 утра - Trim.mp4"  # Используем веб-камеру (можно указать путь к видео)
# UPDATE_INTERVAL = 180  # Вывод статистики каждые 3 минуты
# LINE_Y = 300  # Y-координата линии шлагбаума
# MODEL_PATH = "yolov8n.pt"  # Предобученная YOLOv8 nano (оптимальна для ЦП)
#
# # === Загрузка модели YOLO ===
# model = YOLO(MODEL_PATH)
#
# # === Определение классов ТС ===
# CLASS_MAP = {
#     2: "мотоцикл/велосипед",
#     3: "легковой автомобиль",
#     5: "микроавтобус",
#     7: "автобус",
#     8: "грузовое ТС"
# }
#
# # === Подсчет объектов ===
# vehicles = []
# crossings = []

# === Запуск камеры ===
cap = cv2.VideoCapture("tests/7 утра - Trim.mp4")
start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # # === Запуск YOLO ===
    # results = model(frame)[0]
    #
    # # === Подготовка статистики ===
    # counts = {"от камеры": {"левая полоса": 0, "правая полоса": 0},
    #           "к камере": {"левая полоса": 0, "правая полоса": 0}}
    #
    # # === Обход детекций ===
    # for box in results.boxes.data:
    #     x1, y1, x2, y2, conf, cls = box
    #     cls = int(cls)
    #
    #     # Игнорируем неклассифицируемые объекты
    #     if cls not in CLASS_MAP:
    #         continue
    #
    #     # Определяем центр объекта
    #     cx = int((x1 + x2) / 2)
    #     cy = int((y1 + y2) / 2)
    #
    #     # Определяем полосу движения
    #     lane = "левая полоса" if cx < frame.shape[1] // 2 else "правая полоса"
    #
    #     # Определяем направление (от камеры / к камере)
    #     direction = "от камеры" if cy < frame.shape[0] // 2 else "к камере"
    #
    #     # Увеличиваем счетчик
    #     counts[direction][lane] += 1
    #
    #     # === Отслеживание пересечения линии ===
    #     if LINE_Y - 10 < cy < LINE_Y + 10:
    #         crossings.append({"направление": direction, "время": time.strftime("%H:%M:%S"), "тип ТС": CLASS_MAP[cls]})
    #
    #     # === Визуализация ===
    #     label = f"{CLASS_MAP[cls]} ({conf:.2f})"
    #     cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    #     cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #
    # # === Рисуем линию шлагбаума ===
    # cv2.line(frame, (0, LINE_Y), (frame.shape[1], LINE_Y), (0, 0, 255), 2)
    #
    # # === Вывод статистики раз в 3 минуты ===
    # if time.time() - start_time > UPDATE_INTERVAL:
    #     df = pd.DataFrame.from_dict(counts, orient="index")
    #     print("\n--- Статистика ТС (раз в 3 минуты) ---\n", df)
    #     start_time = time.time()
    #
    # # === Выводим пересечения линии в реальном времени ===
    # for event in crossings:
    #     print(f"[{event['время']}] {event['тип ТС']} пересек линию ({event['направление']})")

    # === Отображение видео ===
    cv2.imshow("Traffic Monitoring", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Очистка ===
cap.release()
cv2.destroyAllWindows()
