import cv2


# stream_url = "https://media.kgd.ru:11936/traffic/trafcam11prol.m3u8" TODO: ffmpeg
# cookies = "domain_sid=nOUG5rsef6R8gyoH2Iyf9%3A1742053449005" # exp 22.03.2025
# cv2.VideoCapture(f"{PATH}|Cookie=domain_sid=nOUG5rsef6R8gyoH2Iyf9%3A1742053449005")
def get_cap():

    paths = {"1": "../tests/7 утра - Trim.mp4",
             "2": "../tests/12 дня - Trim.mp4",
             "3": "../tests/20 вечера - Trim.mp4"}

    while True:
        try:
            selection = input("Выберете источник изображения (1, 2, 3):\n1 - Тест 7:00\n2 - Тест 12:00\n3 - Тест 20:00\n").strip()
            if selection not in {"1", "2", "3"}:
                raise ValueError
            break
        except ValueError:
            print("Неверный формат. Введите только 1, 2 или 3.")

    PATH = paths[selection]

    cap = cv2.VideoCapture(PATH)
    return cap
