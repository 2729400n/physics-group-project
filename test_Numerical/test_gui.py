import Numerical_Methods.GUI as gui
import sys,pytest
import check_user_approval, unittest
class Test_GUI():
    def test_scenes(self):
        assert(check_user_approval.didItWorkAsIntended()==0)
        return None
    def test_show(self):
        gui.start()
        # assert(check_user_approval.didItWorkAsIntendedScale()>5,'Not satisfactory')
        return None

