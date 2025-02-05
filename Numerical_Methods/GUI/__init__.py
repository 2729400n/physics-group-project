import os
import os.path as pth
import slugify

baseDir = pth.abspath(pth.dirname(__file__))
res = dict(scenes={},images={})
scenes = {}
for i in os.listdir(baseDir):
    basename=i.lower()
    item_name = slugify.slugify(basename,entities=False,decimal=False)
    if basename.startswith('gui_scene'):
        mod=__import__(i.removesuffix('.py'),globals=globals(),fromlist=['scenes'],level=1)
        try:
            scenes.update(**mod.scenes)
        except:
            pass
