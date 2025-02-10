import Numerical_Methods.utils as utils

def test_slugs(x:str=None):
    for i in utils.naming.slugify(x):
        assert(i.isalnum() or i =='-' or i=='_')
        