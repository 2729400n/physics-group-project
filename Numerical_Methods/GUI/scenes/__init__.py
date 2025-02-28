import os
import os.path as pth
from ...utils.naming import slugify
from ...utils.importer_lib import import_all_from_path,import_from_path

# Global dictionary to store scenes and images
res = dict(scenes={}, images={})
scenes = res['scenes']

def load_gui_scenes(base_dirs=None):
    """
    This function loads `gui_scene` modules from the given directories and collects their scenes.
    
    Args:
        base_dirs (list): List of directories to search for `gui_scene` modules. Defaults to the current directory if None.
        
    Returns:
        None: The global `scenes` dictionary is updated directly.
    """
    
    # Default to the current directory if no base_dirs provided
    if base_dirs is None:
        base_dirs = [pth.abspath(pth.dirname(__file__))]

    global scenes  # Declare the global scenes variable

    # Loop through each directory to find `gui_scene` files
    for baseDir in base_dirs:
        baseDir = pth.abspath(baseDir)  # Make sure we are working with absolute paths
        
        if not os.path.isdir(baseDir):
            print(f"Warning: {baseDir} is not a valid directory, skipping.")
            continue
        
        for item in os.listdir(baseDir):
            basename = item.lower()
            item_name = slugify(basename)

            # Look for files that match 'gui_scene'
            if basename.startswith('gui_scene') and item.endswith('.py'):
                mod_name = item.removesuffix('.py')
                
                # Import the module dynamically
                try:
                    mod = import_from_path(pth.join(baseDir, item),mod_name=f'Numerical_Methods.GUI.Scenes.{mod_name}')
                    
                    # Update global scenes dictionary with any new scenes from the module
                    if hasattr(mod, 'scenes'):
                        scenes.update(mod.scenes)
                    else:
                        print(f"Warning: {mod_name} does not contain 'scenes' attribute.")
                    
                except ImportError as e:
                    print(f"Error importing {mod_name}: {e}")
                except Exception as e:
                    print(f"Unexpected error with {mod_name}: {e}")

# Example Usage
if __name__ == '__main__':
    # Specify custom directories here, or leave empty to search the current directory
    directories_to_search = ['path/to/dir1', 'path/to/dir2']
    
    # Call the function to update the global scenes dictionary
    load_gui_scenes(base_dirs=directories_to_search)
    
    # Print all scenes loaded
    import pprint
    pprint.pprint(scenes)
else:
    # load_gui_scenes()
    pass