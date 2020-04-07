#==============================================================================#
#                             INTPROG Coursework 1                             #
#                    Python Coursework: A Patchwork Sampler                    #
#==============================================================================#
# Student: UP847232                                                            #
#==============================================================================#

from graphics import*
penPatchSet = []
finPatchSet = []
colourPoints = []

def main():
    size, colours, validColours = getInputs()
    win = drawPatchwork(size, colours)
    selectPatch(win, validColours)

def getInputs():
    size = getSize()
    colours, validColours = getColours()
    return size, colours, validColours

def getSize():
    validSizes = ["5", "7", "9"]
    size = ""
    while size not in validSizes:
        print("The valid sizes are", end=" ")
        print(*validSizes, sep=", ")
        size = input("Enter a valid size: ")
    print("The chosen size is:", size, "\n")
    return int(size)

def getColours():
    validColours = ["red", "orange", "green", "blue", "magenta", "pink"]
    colours = []
    colour = ""
    for num in ["1st", "2nd", "3rd"]:
        while colour not in validColours:
            print("The available colours are", end=" ")
            print(*validColours, sep=", ")
            colour = input("Enter a vaild colour: ")
        print("{0} chosen colour is: {1} \n".format(num, colour))
        validColours.remove(colour)
        colours.append(colour)
    validColours = validColours + colours
    print("The chosen colours are:", *colours, "\n")
    return colours, validColours

def drawPatchwork(size, colours):
    win = GraphWin("Test Graph", size * 100, size * 100)
    win.setCoords(0, size, size, 0)
    pointTotal, points6th = patchworkCalculator(size)
    patchworkSetter(win, size, colours, pointTotal, points6th)
    return win

def patchworkCalculator(size):
    pointTotal = []
    points6th = []
    for y in range(size):
        pointCounter = []
        for x in range(size):
            pointCounter.append((x, y))
            pointTotal.append((x,y))
        points6th = points6th + pointCounter[y: size - y]
        if y >= (size // 2):
            points6th = points6th + pointCounter[size - (y + 1): y + 1]
    return pointTotal, points6th

def patchworkSetter(win, size, colours, pointTotal, points6th):
    for position in pointTotal:
        x = position[0]
        y = position[1]
        if position in points6th:
            drawFinPatch(win, colours[0], x, y)
        elif x <= (size // 2):
            drawPenPatch(win, colours[1], x, y)
        else:
            drawPenPatch(win, colours[2], x, y)

def drawPenPatch(win, colour, axisX, axisY):
    colours = ["white", colour]
    for i in range(5):
        for j in range(5):
            x = (j * 0.2) + axisX
            y = (i * 0.2) + axisY
            centre = Point(x + 0.1, y + 0.1)
            tri_x = x + (0.2 * ((i + 1) % 2))
            colourSelect = (i + j) % 2
            square = drawSquare(win, colours[colourSelect],
                                     colours[colourSelect], x, y, 0.2, 1)
            patch = [square]
            if colourSelect == 0:
                head = Circle(centre, 0.1)
                head.setOutline(colour)
                head.setFill(colour)
                head.draw(win)
                mouth = Polygon(centre, Point(tri_x , y), Point(tri_x, y + 0.2))
                mouth.setOutline("White")
                mouth.setFill("White")
                mouth.draw(win)
                patch.append(head)
                patch.append(mouth)
            penPatchSet.append(patch)
    attributes = [(axisX, axisY), colour]
    colourPoints.append(attributes)

def drawFinPatch(win, colour, axisX, axisY):
    for i in range(5):
        for j in range(5):
            x = (j * 0.2) + axisX
            y = (i * 0.2) + axisY
            square = drawSquare(win, colour, "white", x, y, 0.2, 1)
            message = Text(Point(x + 0.1, y + 0.1), "hi!")
            message.setFill(colour)
            message.setSize(5)
            message.draw(win)
            patch = [square, message]
            finPatchSet.append(patch)
    attributes = [(axisX, axisY), colour]
    colourPoints.append(attributes)

def drawSquare(win, outColour, fillColour, x, y, space, width):
    square = Rectangle(Point(x, y), Point(x + space, y + space))
    square.setOutline(outColour)
    square.setWidth(width)
    square.setFill(fillColour)
    square.draw(win)
    return square

#==============================================================================#
#                                Challenge Part                                #
#==============================================================================#

def selectPatch(win, validColours):
    while True:
        print("To select a patch to modify click with the left mouse button")
        click = win.getMouse()
        for i in range(5):
            for j in range(5):
                if j < click.getX() < (j + 1) and i < click.getY() < (i + 1):
                    border = drawSquare(win, "black", "", j, i, 1, 5)
                    checkKeys(win, j, i, validColours)
                    border.undraw()

def checkKeys(win, x, y, validColours):
    key = ""
    removeKeys = ["s", "d"]
    print("Use the keys to modify the selected patch. The valid keys are:")
    print("S = switches the patch design")
    print("D = deletes the patch")
    print("Enter = deselects the patch")
    print("B, G, M, O, P, R = creates a new patch of the selected colour \n")
    while key != "Return":
        key = win.getKey()
        status, patchList = checkCell(x, y)
        for col in validColours:
            if key in removeKeys and status == "Patched":
                group, colour = deletePatch(win, patchList, x, y)
                if key == "s":
                    if group == "FIN":
                        drawFinPatch(win, colour, x, y)
                    elif group == "PEN":
                        drawPenPatch(win, colour, x, y)
            elif key == col[0] and status == "Blank":
                keyColour = col
                drawFinPatch(win, keyColour, x, y)

def checkCell(x, y):
    status = "Blank"
    patchList = []
    for patch in (penPatchSet + finPatchSet):
        centre = patch[0].getCenter()
        pX = centre.getX()
        pY = centre.getY()
        if x < pX < (x + 1) and y < pY < (y + 1):
            status = "Patched"
            patchList.append(patch)
    return status, patchList

def deletePatch(win, patchList, x, y):
    group = ""
    colour = ""
    for values in colourPoints:
        if (x, y) == values[0]:
            colour = values[1]
    for patch in patchList:
        if patch in penPatchSet:
            penPatchSet.remove(patch)
            group = "FIN"
        elif patch in finPatchSet:
            finPatchSet.remove(patch)
            group = "PEN"
        for part in patch:
            part.undraw()
    return group, colour

main()