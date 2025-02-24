import PIL.Image as Image


def saveImage(file,img:Image.ImageFile.ImageFile):
    img.save(file,format='png')
    
def openImage(filename,*args,**kwargs):
    img=Image.open(fp=filename,mode='r')
    return img

fileOps = {'open':openImage,'save':saveImage}
name = 'Image'
extensions = ['.png','.jpeg','.jpg','.bmp']