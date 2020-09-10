import numpy as np
import cv2


def resizeImage(img, height):
    width = round(img.shape[1] * (height/img.shape[0]))
    return cv2.resize(img,(height,width))


def pad_image(img, border = 10):
    img =  cv2.copyMakeBorder(img, border, border, border, border, cv2.BORDER_CONSTANT, None, 255)
    return img

def noise_removal(image):
    kernel = getKernel(image)
    return cv2.erode(
        cv2.dilate(image, kernel)
        , kernel
    )

def getNumberRect(img):
    gray = 255 * (img < 128).astype(np.uint8)  # To invert the text to white
    coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
    return (x, y, w, h)

def isWhiteImage(image):
    return np.all(image == 255)


def draw_white_border(image):
    white = (255, 255, 255)
    h, w = image.shape[0] - 1, image.shape[1] - 1
    verticalEdge, horizontalEdge = h // 4, w // 4
    thickness = max([verticalEdge, horizontalEdge])

    return cv2.rectangle(image, (0, 0), (w, h), white, thickness)

def getKernel(image):
    dim = max(image.shape) // 20
    if dim < 3:
        dim = 3

    return np.ones((dim, dim), np.uint8)

def rowCol(i):
    return i // 9 + 1, i % 9 + 1

def order_corner_points(corners):
    # Separate corners into individual points
    # Index 0 - top-right
    #       1 - top-left
    #       2 - bottom-left
    #       3 - bottom-right
    corners = [(corner[0][0], corner[0][1]) for corner in corners]
    corners  = sorted(corners, key = lambda x : x[1])
    top_corners, bottom_corners = sorted(corners[0:2],key = lambda x:x[0]), sorted(corners[2:],key = lambda x:x[0])
    top_l,top_r = top_corners
    bottom_l,bottom_r = bottom_corners
    return (top_l, top_r, bottom_r, bottom_l)

def perspective_transform(image, corners):

    # Order points in clockwise order
    ordered_corners = order_corner_points(corners)
    top_l, top_r, bottom_r, bottom_l = ordered_corners

    # Determine width of new image which is the max distance between
    # (bottom right and bottom left) or (top right and top left) x-coordinates
    width_A = np.sqrt(((bottom_r[0] - bottom_l[0]) ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
    width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
    width = max(int(width_A), int(width_B))

    # Determine height of new image which is the max distance between
    # (top right and bottom right) or (top left and bottom left) y-coordinates
    height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) + ((top_r[1] - bottom_r[1]) ** 2))
    height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) + ((top_l[1] - bottom_l[1]) ** 2))
    height = max(int(height_A), int(height_B))

    # Construct new points to obtain top-down view of image in
    # top_r, top_l, bottom_l, bottom_r order
    dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                    [0, height - 1]], dtype = "float32")

    # Convert to Numpy format
    ordered_corners = np.array(ordered_corners, dtype="float32")

    # Find perspective transform matrix
    matrix = cv2.getPerspectiveTransform(ordered_corners, dimensions)

    # Return the transformed image
    return cv2.warpPerspective(image, matrix, (width, height))

def get_largest_box(image, isGray = True):
    if not isGray: image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    ROI_number = 0
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)

        if len(approx) == 4:
            return c,approx

def cropImage(image, isGray = True):
    original = np.copy(image)
    contour, corners = get_largest_box(original,isGray)
    transformed = perspective_transform(original, corners)
    # rotated = rotate_image(transformed,0)
    return transformed

def cropImageToCorners(image,corners):
    transformed = perspective_transform(image,corners)
    return transformed

def crop_to_number(cell, padding = True):
    numberRect = getNumberRect(cell)
    x, y, w, h = numberRect
    cell = cell[y:y + h, x:x + w]
    if padding : cell = pad_image(cell)
    return cell

def add_image_onto(cell, solved_cell_image):
    height,width,_ = cell.shape
    x_offset = int((width - solved_cell_image.shape[1]) / 2)
    y_offset = int((height - solved_cell_image.shape[0]) / 2)

    cell[y_offset:y_offset + solved_cell_image.shape[0], x_offset:x_offset + solved_cell_image.shape[1]] = solved_cell_image
    return cell

def show(img):
    cv2.imshow("",img)
    cv2.waitKey(0)

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)