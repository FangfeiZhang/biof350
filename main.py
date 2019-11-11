import cv2
import numpy
from PIL import Image, ImageTk
from Tkinter import Tk, Canvas
from commands import getoutput
import sys
#import commands
"""
img = cv2.imread("original/1.png", 0)
#blur = cv2.GaussianBlur(img, (5,5), 0)
retval, img_bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
print(retval)
img_bw = cv2.bitwise_not(img_bw)

kernel = numpy.ones((5,5), numpy.uint8)
errosion = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, kernel)
#errosion = cv2.erode(img_bw, kernel, iterations=1)
import
cv2.imwrite("bw.png", cv2.bitwise_not(img_bw))
"""
image_dir = "original/"
save_dir = "save/"
Kernel = 20
threshold = -1
ANCHOR_X = -5000
ANCHOR_Y = -2000
Test_number = 4
go = True  
run = False
#close files and save file
def Convert(file, kernel, in_dir, out_dir, dilation = False, size = 0, threshold = -1):
    Kernel = numpy.ones((kernel, kernel), numpy.uint8)
    img = cv2.imread(in_dir+file, 0)

    if threshold <= 0:
        threshold, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    print(threshold)

    img_bw = cv2.bitwise_not(img)
    img_bw = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, Kernel)
    #   closing = cv2.erode(img_bw, Kernel, iterations=1)
    if dilation == True:
        dilation_kernel = numpy.ones((size, size), numpy.uint8)
        img_bw = cv2.erode(img_bw, dilation_kernel, iterations=1) 
        
    cv2.imwrite(out_dir+"temp" + file, cv2.bitwise_not(img_bw))


origContent = [i for i in getoutput("ls " + image_dir).split()]
saveContent = [i for i in getoutput("ls " + save_dir).split()]

"""
for i in origContent:
    Convert(i, Kernel, image_dir, save_dir)
"""
if(go == True):
    for i in range(Test_number):
        Convert(origContent[i], Kernel, image_dir, save_dir)
#Convert(content[2], Kernel, image_dir, save_dir)


def floodFill(x, y, z, color, image):
    frontier = [(x, y, z)]
    width, height = image[z].size
    counter = 0
    while len(frontier) != 0:
        img_x, img_y, curr = frontier.pop()
        image[curr].putpixel((img_x, img_y), color)
        if counter % 100000 == 0:
            image[curr].save(save_dir+str(curr)+".png")
            print("write")
        neighbors = [(img_x + 1, img_y, curr),
                     (img_x - 1, img_y, curr),
                     (img_x, img_y + 1, curr),
                     (img_x, img_y - 1, curr),  
                     (img_x, img_y, curr + 1),
                     (img_x, img_y, curr - 1)]
        for n in neighbors:
            nx, ny, nz = n
            if nx >= width or nx < 0:
                continue
            if ny >= height or ny < 0:
                continue
            if nz >= len(image) or nz < 0:
                continue
            if image[nz].getpixel((nx, ny)) == (255, 255, 255):
                frontier.append(n)
        counter += 1
    return image

def canvasFill(event, z, color, image):
    global origContent, save_dir
    temp = floodFill(event.x-ANCHOR_X, event.y-ANCHOR_Y, z, color, image)
    for i in range (len(temp)):
        temp[i].save(save_dir+origContent[i])
    print("done")

if run == True:
    imageStack = [Image.open(save_dir +fn).convert("RGB") for fn in saveContent]


    app = Tk()
    app.resizable(True, True)
    canvas = Canvas(app)
    canvas.pack()
    canvas['width'], canvas['height'] = imageStack[0].size
    pimg = ImageTk.PhotoImage(image=imageStack[0])
    canvas.create_image(ANCHOR_X, ANCHOR_Y, anchor='nw', image = pimg)

    canvas.bind("<Button-1>", lambda e : canvasFill(e, 0, (255, 0, 125), imageStack))


    app.mainloop()

#print (content)
