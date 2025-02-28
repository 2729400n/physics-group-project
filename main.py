import time
import Numerical_Methods.GUI as gui
import Numerical_Methods.utils.check_user_approval as check_user_approval
import Numerical_Methods.utils.realtime as rtLoader
import Numerical_Methods.utils.cleancaches as cachecleaner
import sys
import Numerical_Methods
import pathlib
class TestGUI:
    """A Class used for testing implementation of the GUI."""

    def test_scenes(self):
        """Test if the user approval function works correctly."""
        assert check_user_approval.didItWorkAsIntended() == 0

    def test_show(self):
        """Start the GUI for testing."""
        gui.start()


if __name__ == "__main__":
    
    # clear_cache  = check_user_approval.wouldYouLike(
    #     "Would you like to clear cached files in this Package?"
    # )
    # if clear_cache:
    #     numerical_methods_path =pathlib.Path(Numerical_Methods.__file__).resolve().absolute()
    #     if(numerical_methods_path.is_dir()):
    #         cachecleaner.clearPythonCaches(numerical_methods_path)
    #     else:
    #         cachecleaner.clearPythonCaches(numerical_methods_path.parent)
            
    
    caching = check_user_approval.wouldYouLike(
        "Would you like to enable Python caching? It makes for speedy re runs!"
    )
    
    if caching:
        sys.dont_write_bytecode=True
    else:
        sys.dont_write_bytecode=False
    
    
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
