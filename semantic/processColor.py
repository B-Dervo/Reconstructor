import os
import PIL
import shutil
from PIL import Image





#im = Image.open("Ba_b_do8mag_c6_big.png")
#rgb_im = im.convert('RGB')
#rgb_im.save('colors.jpg')

def changeFormat(folder):
    try:
        shutil.rmtree("tmp/"+folder+"/color2/")
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    os.mkdir("tmp/"+folder+"/color2/")

    for target in os.listdir("tmp/"+folder+"/color/"):
        #print(target)
        im = Image.open("tmp/"+folder+"/color/"+target)
        rgb_im = im.convert("RGB")
        rgb_im = PIL.ImageOps.invert(rgb_im)# change to white = no crack & black = crack
        rgb_im.save("tmp/"+folder+"/color2/"+target[:-4]+".jpg")