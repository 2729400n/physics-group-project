import Numerical_Methods.GUI.gui_window_main as mainWin
import sys,pytest
class Test_GUI():
    def test_scenes(self):
        print(self,flush=True,file=sys.stderr)
        sys.stderr.write('Hello')
        raise Exception(self.__str__())
    def test_show(self):
        mainWin.testProd()