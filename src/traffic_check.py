import cv2


def is_inside_polygon(point, polygon):
    polygon = polygon[0] # Забираем только точки
    polygon = polygon.reshape((-1, 1, 2)) # Для pointPolygonTest()
    return cv2.pointPolygonTest(polygon, point, False) >= 0