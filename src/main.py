import cv2
import time
from copy import deepcopy
from prettytable import PrettyTable

from capture import get_cap
from markup import polygons, lines, lanes
from models.yolov8n import yolo8vn
from utils import is_inside_polygon
from cls import CLASS_MAP
from counts import counts_template

def main():
    # Инициализация переменных и массивов
    cap = get_cap() # Инициализация захвата видео
    model = yolo8vn # Инициализация модели
    top_to_bottom_traffic = None  # Флаг на направление трафика
    frame_count = 0

    # Открытие видео
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

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
        results = model(frame)[0] # Детекции

        # Обход детекций
        counts = deepcopy(counts_template) # Подсчеты объектов на фрейме
        for box in results.boxes.data:
            x1, y1, x2, y2, conf, cls = box
            center = (int((x1 + x2) / 2), int((y1 + y2) / 2)) # Центр объекта
            cls = int(cls) # Для корректной работы с картой классов
            if cls not in CLASS_MAP: # Не работаем с нецелевыми объектами
                continue

            # Определяем изменение направления движения трафика
            if is_inside_polygon(center, polygons["to-bottom-check"]) or is_inside_polygon(center, polygons["to-top-check"]):
                top_to_bottom_traffic = True
            elif is_inside_polygon(center, polygons["to-right-check"]) or is_inside_polygon(center, polygons["to-left-check"]):
                top_to_bottom_traffic = False

            # Считаем количество объекта по линиям
            if top_to_bottom_traffic is True: # Такое большое кол-во проверок для того, чтобы уменьшить кол-во вызовов is_inside_polygon()
                if is_inside_polygon(center, lanes["to-top"]):
                    if is_inside_polygon(center, lanes["to-top-right-lane"]):
                        counts["top-bottom"]["to-top"]["to-top-right-lane"][CLASS_MAP[cls]] += 1
                    elif is_inside_polygon(center, lanes["to-top-left-lane"]):
                        counts["top-bottom"]["to-top"]["to-top-left-lane"][CLASS_MAP[cls]] += 1
                elif is_inside_polygon(center, lanes["to-bottom"]):
                    if is_inside_polygon(center, lanes["to-bottom-right-lane"]):
                        counts["top-bottom"]["to-bottom"]["to-bottom-right-lane"][CLASS_MAP[cls]] += 1
                    elif is_inside_polygon(center, lanes["to-bottom-left-lane"]):
                        counts["top-bottom"]["to-bottom"]["to-bottom-left-lane"][CLASS_MAP[cls]] += 1
            elif top_to_bottom_traffic is False:
                if is_inside_polygon(center, lanes["to-left"]):
                    if is_inside_polygon(center, lanes["to-left-right-lane"]):
                        counts["left-right"]["to-left"]["to-left-right-lane"][CLASS_MAP[cls]] += 1
                    elif is_inside_polygon(center, lanes["to-left-left-lane"]):
                        counts["left-right"]["to-left"]["to-left-left-lane"][CLASS_MAP[cls]] += 1
                elif is_inside_polygon(center, lanes["to-right"]):
                    if is_inside_polygon(center, lanes["to-right-right-lane"]):
                        counts["left-right"]["to-right"]["to-right-right-lane"][CLASS_MAP[cls]] += 1
                    elif is_inside_polygon(center, lanes["to-right-left-lane"]):
                        counts["left-right"]["to-right"]["to-right-left-lane"][CLASS_MAP[cls]] += 1

        # Вывод информации
        if top_to_bottom_traffic is True:
            from prettytable import PrettyTable

            data = {
                "top-bottom": {
                    "to-top": {
                        "to-top-right-lane": {"bike": 0, "car/van": 0, "bus": 0, "cargo": 0},
                        "to-top-left-lane": {"bike": 0, "car/van": 0, "bus": 0, "cargo": 0},
                    },
                    "to-bottom": {
                        "to-bottom-right-lane": {"bike": 0, "car/van": 0, "bus": 0, "cargo": 0},
                        "to-bottom-left-lane": {"bike": 0, "car/van": 0, "bus": 0, "cargo": 0},
                    },
                }
            }

            table = PrettyTable()
            table.field_names = ["Direction", "Lane", "Bike", "Car/Van", "Bus", "Cargo"]

            for direction, lanes in data.items():
                for move, lane_dict in lanes.items():
                    for lane, counts in lane_dict.items():
                        table.add_row([f"{direction} -> {move}", lane, counts["bike"], counts["car/van"], counts["bus"],
                                       counts["cargo"]])

            print(table)

        elif top_to_bottom_traffic is False:
            pass

            # # Визуализация боксов
            # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            # cv2.circle(frame, center, radius=10, color=(15, 245, 76), thickness=2)

        # Вывод изображения
        cv2.imshow("Traffic Monitoring", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

        if top_to_bottom_traffic is True:
            print('Сверху-вниз')
        elif top_to_bottom_traffic is False:
            print('Слева-направо')
        else:
            print('None')


    # Завершение работы
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()