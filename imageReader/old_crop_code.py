def checkHorizontalBlackLine(image, currentY, dimensions):
    h, w = dimensions

    xPoints = np.arange(0, w)
    colours = {'black': 0, 'white': 0}
    for x in xPoints:
        pixel = image[currentY, x]

        if pixel == 0:
            colours['black'] += 1
        else:
            colours['white'] += 1

    return colours['black'] > colours['white']


def checkVerticalBlackLine(image, currentX, dimensions):
    h, w = dimensions

    yPoints = np.arange(0, h)
    colours = {'black': 0, 'white': 0}
    for y in yPoints:
        pixel = image[y, currentX]

        if pixel == 0:
            colours['black'] += 1
        else:
            colours['white'] += 1

    return colours['black'] > colours['white']

def cropImage_old(image):
    h, w = image.shape[0] - 1, image.shape[1] - 1

    xmin, xmax, ymin, ymax = 0, w, 0, h

    currentY = ymin
    while not checkHorizontalBlackLine(image, currentY, (h, w)) and currentY < h:    currentY += 1

    while checkHorizontalBlackLine(image, currentY, (h, w)) and currentY < h:        currentY += 1
    ymin = currentY

    currentY = ymax
    while not checkHorizontalBlackLine(image, currentY, (h, w)) and currentY > 0:    currentY -= 1

    while checkHorizontalBlackLine(image, currentY, (h, w)) and currentY > 0:        currentY -= 1
    ymax = currentY

    currentX = xmin
    while not checkVerticalBlackLine(image, currentX, (h, w)) and currentX < w:    currentX += 1

    while checkVerticalBlackLine(image, currentX, (h, w)) and currentX < w:        currentX += 1
    xmin = currentX

    currentX = xmax
    while not checkVerticalBlackLine(image, currentX, (h, w)) and currentX > 0:    currentX -= 1

    while checkVerticalBlackLine(image, currentX, (h, w)) and currentX > 0:        currentX -= 1

    xmax = currentX

    croppedWidth = xmax - xmin
    croppedHeight = ymax - ymin

    crop_img = image[ymin:ymin + croppedHeight, xmin:xmin + croppedWidth]
    return crop_img
