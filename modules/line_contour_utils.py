import cv2

def get_biggest_valid_contour(contours, min_area=1500):
    if not contours:
        return None

    biggest = max(contours, key=lambda contour_data: contour_data[1])
    contour, area = biggest

    if area < min_area:
        return None

    return contour
