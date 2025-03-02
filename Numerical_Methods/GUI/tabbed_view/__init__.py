import tkinter as tk
import tkinter.ttk as ttk
import os
import os.path as pth
import tkinter.dnd as dnd

from ...utils.importer_lib import import_from_path

__base__ = pth.abspath(pth.dirname(__file__))
__base_package__ = pth.abspath(pth.join(__base__, '..', '..'))


class IScene(tk.Widget):
    name: str


class TabbedView(ttk.Notebook):
    def __init__(self, master=None, **kw):
        super().__init__(master, width=640, height=480, **kw)
        self.loaded_scenes = {}
        self.dragging_tab = None  # Track the tab being dragged
        self.drag_start_idx = None  # Start index of the tab being dragged
        self.ordering = ('HOME', 'TASKSOLVER', 'TASK', 'SOLVER', 'HELP')

    def buildTab(self, dir):
        k = 0
        for i in os.listdir(dir):
            # print(i)
            if i.startswith('gui_scene'):

                modname = f'Numerical_Methods.GUI.scenes.{i.removesuffix(".py")}'
                modorigin = pth.join(dir, i)

                scene_module = import_from_path(
                    path=modorigin, mod_name=modname, is_pacakge=False)

                scene = scene_module.__dict__.get('scene')

                if scene is not None:
                    k += 1
                    curr_scene: IScene = scene(self)
                    try:
                        text = curr_scene.__getattribute__('name')
                    except AttributeError:
                        text = f'Tab-{k}'
                    except Exception as e:
                        # print(e)
                        raise e
                    if text in self.loaded_scenes:
                        text = f'Tab-{k}'
                    self.loaded_scenes.update({text: curr_scene})
                else:
                    print(scene_module, 'No Scene')

        for i in self.loaded_scenes:
            self.add(self.loaded_scenes[i],
                     state='normal', sticky='nesw', text=i)
            for ind in range(len(self.ordering)):
                if (self.ordering[ind] in i.upper()) and (ind == 0):

                    self.insert(ind, self.loaded_scenes[i])
                    if ind == 0:
                        self.select(self.loaded_scenes[i])

        self.bind('<Button-1>', self.resize_subviews)
        # self.bind('<B1-Motion>', self.on_drag_motion)
        # self.bind('<ButtonRelease-1>', self.on_drop)

    def on_drag_start(self, event):
        """Starts the drag process when a tab is clicked."""
        tabindex = self.index(f'@{event.x},{event.y}')
        self.drag_start_idx = tabindex
        self.dragging_tab = self.tab(self.drag_start_idx)
        # print(f"Dragging started for tab {self.dragging_tab}")

    def on_drag_motion(self, event):
        """Handles the dragging motion (tab following the mouse)."""
        if self.dragging_tab:
            # Find the tab index where the tab is being dropped
            drop_index = None
            try:
                drop_index = self.index(f'@{event.x},{event.y}')
            except Exception:
                return
            if (drop_index != self.drag_start_idx) and (drop_index is not None):
                # print(f"Dropped tab at index {drop_index}")
                # Rearrange the tabs
                # dropped_at = self.tab(drop_index)
                self.insert(drop_index, self.tabs()[self.drag_start_idx])
                self.drag_start_idx = drop_index
            pass

    def on_drop(self, event):
        """Handles the drop of the tab at a new location."""
        if self.dragging_tab:
            # Find the tab index where the tab is being dropped
            drop_index = None
            try:
                drop_index = self.index(f'@{event.x},{event.y}')
            except Exception:
                self.dragging_tab = None
                self.drag_start_idx = None
                return
            if (drop_index != self.drag_start_idx) and (drop_index is not None):
                # print(f"Dropped tab at index {drop_index}")
                # Rearrange the tabs
                # dropped_at = self.tab(drop_index)
                self.insert(drop_index, self.tabs()[self.drag_start_idx])

            # Reset dragging state
            self.dragging_tab = None
            self.drag_start_idx = None

    def dnd_accept(self, src, evt):
        self.on_drag_motion(evt)

    def dnd_enter(self, *args, **kwargs):
        # print('dnd_enter', args, kwargs)
        pass

    def dnd_leave(self, *args, **kwargs):
        # print('dnd_leave', args, kwargs)
        pass

    def dnd_motion(self, *args, **kwargs):
        # print('dnd_motion', args, kwargs)
        pass

    def dnd_drop(self, *args, **kwargs):
        # print('dnd_drop', args, kwargs)
        pass

    def dnd_commit(self, *args, **kwargs):
        # print('dnd_commit', args, kwargs)
        pass

    def dnd_start(self, src, evt):
        # print('dnd_start', evt)
        pass

    def dnd_end(self, src, evt):
        self.on_drop(evt)
        pass

    def resize_subviews(self, evt: 'tk.Event[tk.Frame]'):
        try:
            self.on_drag_start(evt)
            dnd.dnd_start(self, event=evt)
        except Exception:
            return


if __name__ == '__main__':
    root = tk.Tk()
    tabsolder = TabbedView(root)
    dndEvent = tk.Event()
    dndEvent.widget = tabsolder
    tabsolder.buildTab(pth.abspath(pth.join(__base__, '../scenes')))
    root.mainloop()
