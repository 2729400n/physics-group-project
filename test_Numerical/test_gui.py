import Numerical_Methods.GUI.gui_window_main as mainWin
import sys,pytest
import check_user_approval, unittest
class Test_GUI():
    def test_scenes(self):
        assert(check_user_approval.didItWorkAsIntended()==0)
        return 0
    def test_show(self):
        mainWin.testProd()
        assert(check_user_approval.didItWorkAsIntendedScale()>5,'Not satisfactory')
        return 0
@unittest.FunctionTestCase
def test_canvas():
    pass