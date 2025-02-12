import Numerical_Methods
import Numerical_Methods.GUI.scenes as gui, Numerical_Methods.GUI.py_iface as pyface
import Numerical_Methods.Boundaries as bounds
import argparse, sys

parser =argparse.ArgumentParser(bounds.boundary1.__name__)
parser.add_argument('filename',action='extend',nargs='*',)
nspace:argparse.Namespace=parser.parse_args(sys.argv[1:])
print()
args = pyface.getArgsToType(func=bounds.boundary1)


for name in args:
    parser.add_argument(name,type=args[name])
    
parser.print_help()