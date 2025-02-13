import Numerical_Methods.GUI as gui
import sys
import test_Numerical.check_user_approval as check_user_approval
import unittest
import pytest
class Test_GUI():
    def test_scenes(self):
        assert(check_user_approval.didItWorkAsIntended()==0)
        return None
    def test_show(self):
        gui.start()
        # assert(check_user_approval.didItWorkAsIntendedScale()>5,'Not satisfactory')
        return None

if __name__ == "__main__":
    tester = Test_GUI()
    tester.test_show()