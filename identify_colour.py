import csv
import sys

import cv2


def mouseRGB(
    event, x,y,flags,param
):
    if event == cv2.EVENT_LBUTTONDOWN:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y,x]
        b, g, r = int(b), int(g), int(r)


def get_colour(
    target_r, # rgb values (0 - 255)
    target_g, # rgb values (0 - 255)
    target_b, # rgb values (0 - 255)
    colour_data # list of dictionaries containing details on each colour
):
    minrgb = 10000
    for index, colour in enumerate(colour_data):
        diff = (
            abs(target_r - int(colour.get("R"))) +
            abs(target_g - int(colour.get("G"))) +
            abs(target_b - int(colour.get("B")))
        )
        if diff < minrgb:
            minrgb = diff
            matched_colour = colour

    return matched_colour


def display_text(img, text, colour):
    cv2.putText(
        img, text, 
        (50,50), # starting position
        2, # font style (0-7)
        0.8, # font scale
        colour, 
        2, # thickness
        cv2.LINE_AA #linetype
    )


try:
    image_path = sys.argv[1]
except IndexError:
    print("Image path required as command line argument")

with open("colours.csv") as colours_csv:
    reader = csv.DictReader(colours_csv, fieldnames=["colour", "colour_name", "hex", "R", "G", "B"])
    colour_data = [row for row in reader]


# global variables, because this library is ridiculous
b = g = r = xpos = ypos = 0
clicked = False 

# parse image file, create window and assign 
img = cv2.imread(image_path)
cv2.namedWindow("Colour Finder")
cv2.setMouseCallback("Colour Finder", mouseRGB)

while True:
    cv2.imshow("Colour Finder", img)
    if clicked:
        colour_name = get_colour(r, g, b, colour_data).get("colour_name")
        colour_hex = get_colour(r, g, b, colour_data).get("hex")

        # text to display over image
        text = f"{colour_name}   R={r} G={g} B={b}"

        # makes rectangle in colour selected to go over
        cv2.rectangle(
            img, # image file to load rectangle onto
            (30,20), # start position of rectangle
            (700,65), # size of rectangle
            (b,g,r), # colour of rectangle
            -1 # thickness
        )
        
        # text displayed in white, unless background colour is very pale where text will be black
        if(sum([r, g, b]) >= 600):
            display_text(img, text, (0,0,0))
        else:
            display_text(img, text, (255,255,255))

        clicked=False

    # ends program and destroys resources when user hits "Q" or "Esc"
    k = cv2.waitKey(1)
    if k in (27, ord("q"), ord("Q")):
        cv2.destroyAllWindows()
        break
