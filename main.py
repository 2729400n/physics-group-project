import time
import Numerical_Methods.GUI as gui
import test_Numerical.check_user_approval as check_user_approval
import Numerical_Methods.utils.realtime as rtLoader
import sys.

class TestGUI:
    """A Class used for testing implementation of the GUI."""

    def test_scenes(self):
        """Test if the user approval function works correctly."""
        assert check_user_approval.didItWorkAsIntended() == 0

    def test_show(self):
        """Start the GUI for testing."""
        gui.start()


if __name__ == "__main__":
    enable_rtloader = check_user_approval.wouldYouLike(
        "Would you like to enable RTLoader?\nIt allows for real-time reloading of Python modules!"
    )

    if enable_rtloader:
        rtLoader.init_realtime_module()
        rtLoader.start_realtime_module()

    try:
        gui.start()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Exiting gracefully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        if enable_rtloader:
            rtLoader.stop_realtime_module()
        raise
    finally:
        
        exit(0)
