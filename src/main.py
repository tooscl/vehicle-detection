from datetime import datetime, timedelta
import cv2
from copy import deepcopy
from prettytable import PrettyTable

from capture import get_cap
from markup import polygons, lines, lanes
from models.yolov8n import yolo8vn
from utils import is_inside_polygon
from cls import class_map
from counts import counts_template

def main():
    # Гиперпараметры
    DELTA_SECONDS = 5 # Частота вывода информации в секундах
    FRAME_SKIP = 2 # Каждый n кадр, который мы пропускаем
    
    # Инициализация переменных и массивов
    cap = get_cap() # Инициализация захвата видео
    model = yolo8vn # Инициализация модели
    top_to_bottom_traffic = None  # Флаг на направление трафика
    frame_count = 0
    last_time_updated = datetime.now()
    update = False # Флаг на вывод информации

    # Открытие видео
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Работа со счетчиком фреймов
        frame_count += 1
        if frame_count % FRAME_SKIP == 0:
            continue # Пропуск кадров для ускорения работы

        # # Разметка фрейма
        # for polygon in lanes.values():
        #     pts, color = polygon
        #     thikness = 2
        #     cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=thikness)
        # for line in lines.values():
        #     start_point, end_point, color = line
        #     thickness = 2
        #     cv2.line(frame, start_point, end_point, color=color, thickness=thickness)

        # Определение объектов
        results = model(frame, verbose=False)[0] # Детекции (без логов)

        # Обход детекций
        counts = deepcopy(counts_template) # Подсчеты объектов на фрейме
        for box in results.boxes.data:
            x1, y1, x2, y2, conf, cls = box
            center = (int((x1 + x2) / 2), int((y1 + y2) / 2)) # Центр объекта
            cls = int(cls) # Для корректной работы с картой классов
            if cls not in class_map: # Не работаем с нецелевыми объектами
                continue

            # Определяем изменение направления движения трафика
            if is_inside_polygon(center, polygons["to-bottom-check"]) or is_inside_polygon(center, polygons["to-top-check"]):
                top_to_bottom_traffic = True
            elif is_inside_polygon(center, polygons["to-right-check"]) or is_inside_polygon(center, polygons["to-left-check"]):
                top_to_bottom_traffic = False

            # Проверяем нреобходимость выыода информации
            if datetime.now() - last_time_updated >= timedelta(seconds=DELTA_SECONDS):
                update = True
                last_time_updated = datetime.now()

            # Считаем количество объекта по полосам движения
            if update: # Проверяем необходимость
                if top_to_bottom_traffic is True: # Такое большое кол-во проверок для того, чтобы уменьшить кол-во вызовов is_inside_polygon()
                    if is_inside_polygon(center, lanes["to-top"]):
                        if is_inside_polygon(center, lanes["to-top-right-lane"]):
                            counts["top-bottom"]["to-top"]["to-top-right-lane"][class_map[cls]] += 1
                        elif is_inside_polygon(center, lanes["to-top-left-lane"]):
                            counts["top-bottom"]["to-top"]["to-top-left-lane"][class_map[cls]] += 1
                    elif is_inside_polygon(center, lanes["to-bottom"]):
                        if is_inside_polygon(center, lanes["to-bottom-right-lane"]):
                            counts["top-bottom"]["to-bottom"]["to-bottom-right-lane"][class_map[cls]] += 1
                        elif is_inside_polygon(center, lanes["to-bottom-left-lane"]):
                            counts["top-bottom"]["to-bottom"]["to-bottom-left-lane"][class_map[cls]] += 1
                elif top_to_bottom_traffic is False:
                    if is_inside_polygon(center, lanes["to-left"]):
                        if is_inside_polygon(center, lanes["to-left-right-lane"]):
                            counts["left-right"]["to-left"]["to-left-right-lane"][class_map[cls]] += 1
                        elif is_inside_polygon(center, lanes["to-left-left-lane"]):
                            counts["left-right"]["to-left"]["to-left-left-lane"][class_map[cls]] += 1
                    elif is_inside_polygon(center, lanes["to-right"]):
                        if is_inside_polygon(center, lanes["to-right-right-lane"]):
                            counts["left-right"]["to-right"]["to-right-right-lane"][class_map[cls]] += 1
                        elif is_inside_polygon(center, lanes["to-right-left-lane"]):
                            counts["left-right"]["to-right"]["to-right-left-lane"][class_map[cls]] += 1
                else:
                    pass

        # Вывод информации
        if update: # Проверка на необходимость
            print("\n=== CURRENT STATE ===")
            print(f"TIME: {datetime.now()}") # Когда работаем с прямой трансляцией
            print(f"FRAME: {frame_count}")
            if top_to_bottom_traffic is True:
                print("TRAFFIC DIRECTION: top-bottom")
                data = counts["top-bottom"]
                table = PrettyTable()
                table.field_names = ["Direction", "Lane", "Bike", "Car/Van", "Bus", "Cargo"]
                for move, lane_dict in data.items():
                    for lane_key, counts in lane_dict.items():
                        table.add_row(
                            [f"{move}", "-".join(lane_key.split("-")[2:]), str(counts["bike"]), str(counts["car/van"]), str(counts["bus"]),
                            str(counts["cargo"])])
                print(table)
            elif top_to_bottom_traffic is False:
                print("TRAFFIC DIRECTION: left-right")
                data = counts["left-right"]
                table = PrettyTable()
                table.field_names = ["Direction", "Lane", "Bike", "Car/Van", "Bus", "Cargo"]
                for move, lane_dict in data.items():
                    for lane_key, counts in lane_dict.items():
                        table.add_row(
                            [f"{move}", "-".join(lane_key.split("-")[2:]), str(counts["bike"]), str(counts["car/van"]),
                             str(counts["bus"]),
                             str(counts["cargo"])])
                print(table)
            update = False # Обнуляем флаг

            # # Визуализация боксов
            # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            # cv2.circle(frame, center, radius=10, color=(15, 245, 76), thickness=2)

        # Вывод изображения
        cv2.imshow("Traffic Monitoring", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Завершение работы
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()