import random
_SuperCrptoRandGen =  random.SystemRandom()

# a relatively cheap slugify implement
def slugify(text:str=None,max_width:int=32,exempt='-'):
    if text is None or text=='':
        width=random.randint(4,max_width)
        text=''.join(_SuperCrptoRandGen.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-',k=width))
        
    out=''
    for i in range(min(len(text),max_width)):
        out+=text[i] if text[i].isalnum() or (text[i] in exempt) else '_'
    return out
