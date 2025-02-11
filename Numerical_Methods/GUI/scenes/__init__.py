import os
import os.path as pth

from ...utils.naming import slugify


baseDir = pth.abspath(pth.dirname(__file__))
res = dict(scenes={},images={})
scenes = {}
for i in os.listdir(baseDir):
    basename=i.lower()
    item_name = slugify(basename)
    if basename.startswith('gui_scene'):
        mod=__import__(i.removesuffix('.py'),globals=globals(),fromlist=['scenes'],level=1)
        try:
            scenes.update(**mod.scenes)
        except:
            pass
import pprint
pprint.pprint(scenes)
del pprint
