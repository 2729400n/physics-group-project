import PIL.Image as Image


def saveImage(file,img:Image.ImageFile.ImageFile):
    img.save(file,format='png')