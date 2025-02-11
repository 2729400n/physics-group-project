import Numerical_Methods
import Numerical_Methods.GUI as gui, Numerical_Methods.GUI.py_iface as pyface
import Numerical_Methods.Boundaries as bounds
import argparse, sys

parser =argparse.ArgumentParser(sys.argv[0])
parser.add_argument()

pyface.getArgsToType(func=bounds.boundary1)


