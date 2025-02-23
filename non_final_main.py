import time
import Numerical_Methods.GUI as gui
import test_Numerical.check_user_approval as check_user_approval
import Numerical_Methods.utils.realtime as rtLoader


class Test_GUI():
    '''
    Test_GUI:
        A Class used for testing implementation
    '''
    def test_scenes(self):
        assert (check_user_approval.didItWorkAsIntended() == 0)
        return None

    def test_show(self):
        gui.start()
        return None




if __name__ == "__main__":
    if(check_user_approval.wouldYouLike("Would you like to enable RTLoader?\n It allows for realtime reloading of python modules!")):
        rtLoader.init_realtime_module()
        rtLoader.start_realtime_module()
        try:
            gui.start()
        except KeyboardInterrupt:
            rtLoader.stop_realtime_module()
            exit(0)
        except Exception as e:
            rtLoader.stop_realtime_module()
            raise e
        finally:
            rtLoader.stop_realtime_module()
            exit(1)
    else:
        try:
            gui.start()
        except Exception as e:
            raise e
        finally:
            exit(1)
