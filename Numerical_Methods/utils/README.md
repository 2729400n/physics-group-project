# Utils

## Structure

All utils should be supllied as python files,
there should not be need to implement directory based python modules in utils.
The res directory should be used for resources that utils may require.
The way that res is currently accessed is using the `os` module.

```python
import os
import os.path as pth

resFolder = pth.join(pth.abspath(pth.dirname(__file__)),'res')

del os
del pth
```

## Contents

This sub module should only contain code for things that aren't the focus of the eproject and may be changed over time.
The Example I will use is a way to populate an array or reshape an array as that is not what we want ut it can be used in the
proccess of getting the output we want.

## Proccess

Create module add to init if u want it to be usable through the `utils` Submodule.
