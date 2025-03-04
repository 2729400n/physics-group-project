from tkinter.ttk import Frame, Button
from typing import Callable
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import (
    MouseEvent,
)
import tkinter as tk
from ...Solvers import errors

import numpy as np
import tkinter.messagebox as msgbox
import tkinter.simpledialog as simple_diag

from threading import Thread
from queue import Full, SimpleQueue
from tkinter.filedialog import (
    asksaveasfilename,
)
from ...utils.nfile_io.extensions import numpy_io

# for semmantic porpuses


class EventFullNavigationToolbar2Tk(NavigationToolbar2Tk):
    def zoom(self, *args):
        # print('zoom', args)
        retval = super().zoom(*args)
        self.event_generate("<<Zoom-Clicked>>")
        return retval

    def drag_zoom(self, evt: MouseEvent, *args):
        # print('drag_zoom', evt,args)
        retval = super().drag_zoom(evt, *args)
        self.event_generate("<<Zoom-Drag>>")
        return retval

    def press_zoom(self, *args):
        # print('press_zoom', args)
        retval = super().press_zoom(*args)
        self.event_generate("<<Zoom-Begin>>")
        return retval

    def release_zoom(self, *args):
        # print('release_zoom', args[0])
        retval = super().release_zoom(*args)
        self.event_generate("<<Zoom-End>>")
        return retval

    def mouse_move(self, event):
        # print('mouse_move', event)
        return super().mouse_move(event)

    def mouse_press(self, event):
        # print('mouse_press', event)
        return super().mouse_press(event)

    def mouse_release(self, event):
        # print('release_mouse', event)
        return super().mouse_release(event)

    def back(self, *args):
        retval = super().back(*args)
        self.event_generate("<<Arrow-Back>>")
        return retval

    def forward(self, *args):
        retval = super().forward(*args)
        self.event_generate("<<Arrow-Forward>>")
        return retval

    def home(self, *args):
        retval = super().home(*args)
        self.event_generate("<<Home-Clicked>>")
        return retval

    def pan(self, *args):
        # print('pan', args)
        retval = super().pan(*args)
        self.event_generate("<<Pan-Clicked>>")
        return retval

    def drag_pan(self, event):
        # print('drag_zoom', event)
        retval = super().drag_pan(event)
        self.event_generate("<<Pan-Drag>>")
        return retval

    def press_pan(self, *args):
        # print('press_pan', args)
        retval = super().press_pan(*args)
        self.event_generate("<<Pan-Begin>>")
        return retval

    def release_pan(self, *args):
        # print('release_pan', args)
        retval = super().release_pan(*args)
        self.event_generate("<<Pan-End>>")
        return retval


class InspectFrame(Frame):

    def __init__(
        self,
        parent,
        Grid_obj,
        dx: float,
        dy: float,
        title="",
        xlabel="",
        ylabel="",
        figsize=(8, 8),
        dpi=64,
        *args,
        **frame_kwargs,
    ):
        super().__init__(master=parent, **frame_kwargs)
        figsize = self.figsize = [*figsize]
        self.title_ = title
        self.dpi = dpi
        fig = self.fig = Figure(figsize=(figsize[0], figsize[1]), dpi=dpi)
        ax = self.ax = fig.add_subplot(111)
        Grid_obj = self.Grid_obj = np.array(Grid_obj, copy=True)
        self.zoomedArea = self.Grid_obj
        self.dx = dx
        self.dy = dy

        self.jobRunning = False
        self.job = None
        self.jobqueue: "SimpleQueue[Callable[[],None]]" = SimpleQueue()

        self.Xs = np.arange(0, self.Grid_obj.shape[1] * self.dx, self.dx)
        self.Ys = np.arange(0, self.Grid_obj.shape[0] * self.dy, self.dy)
        self.zoomedXs = self.Xs
        self.zoomedYs = self.Ys

        mainframe = self.mainframe = Frame(self)
        plot_frame = self.plot_frame = Frame(mainframe)
        button_frame = self.button_frame = Frame(mainframe)

        self.propagate(True)
        mainframe.propagate(True)
        plot_frame.propagate(True)
        button_frame.propagate(True)

        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(1, weight=1)
        # Plot data
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(1, weight=1)

        # Embed figure into Tkinter canvas
        canvas = self.canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas_widget = self.canvas = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew")
        canvas_widget.configure(width=640, height=480)
        canvas.draw()
        # Add Navigation Toolbar
        toolbar = self.toolbar = EventFullNavigationToolbar2Tk(
            canvas, plot_frame, pack_toolbar=False
        )

        toolbar.update()
        toolbar.grid(row=1, column=0, sticky="ew")

        toolbar.bind("<<Zoom-End>>", self.select_Smallgrid, "+")
        toolbar.bind("<<Pan-End>>", self.select_Smallgrid, "+")
        toolbar.bind("<<Arrow-Forward>>", self.select_Smallgrid, "+")
        toolbar.bind("<<Arrow-Back>>", self.select_Smallgrid, "+")
        toolbar.bind("<<Home-Clicked>>", self.select_Smallgrid, "+")

        self.calculatePolyNomialButton = Button(
            button_frame,
            text="Polynomial Interpolate",
            command=self.calculatePolyNomial,
        )

        self.calculatePolyNomialButton.pack()

        self.calculateLaplacian = Button(
            button_frame, text="Calulate Laplacian", command=self.findLaplacian
        )

        self.calculateLaplacian.pack()

        button_frame.grid(column=0, row=0)
        plot_frame.grid(column=1, row=0)

        mainframe.pack(anchor=tk.NW, side=tk.TOP, fill=tk.BOTH, expand=True)

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        # self.ax.legend()

        resi, absresi = errors.laplaceify(self.Grid_obj, self.dx, self.dy)
        img=ax.imshow(Grid_obj)
        fig.colorbar(img)
        self.after(500, self.checkQueue)

    def checkQueue(self):
        # print('checkQueue')
        if self.jobRunning:
            return
        try:
            job = self.jobqueue.get_nowait()
            job()
            # print('done')
        except Exception:
            pass
        self.after(500, self.checkQueue)

    def select_Smallgrid(self, evt):
        #        print('Called')
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        data = self.Grid_obj
        ylim = (ylim[1], ylim[0]) if ylim[1] < ylim[0] else (ylim[0], ylim[1])
        xlim = (xlim[1], xlim[0]) if xlim[1] < xlim[0] else (xlim[0], xlim[1])
        # Find the closest indices using searchsorted (binary search)
        x_start_idx = max(0, np.searchsorted(self.Xs, xlim[0]) - 1)
        x_end_idx = min(len(self.Xs), np.searchsorted(self.Xs, xlim[1]))

        y_start_idx = max(0, np.searchsorted(self.Ys, ylim[0]) - 1)
        y_end_idx = min(len(self.Ys), np.searchsorted(self.Ys, ylim[1]))

        # Extract zoomed-in portion of the data
        self.zoomedArea = data[y_start_idx : y_end_idx + 1, x_start_idx : x_end_idx + 1]
        self.zoomedXs = self.Xs[x_start_idx : x_end_idx + 1]
        self.zoomedYs = self.Ys[y_start_idx : y_end_idx + 1]
        # print(f"Zoomed indices: X({x_start_idx}:{x_end_idx}),
        # Y({y_start_idx}:{y_end_idx})")
        # print(f"Extracted zoomed array:\n{zoomed_data}")

    def showAndOfferSavePolyNomial(self, message, **data):
        def __inner_func() -> None:
            nonlocal message, data
            dsimple = simple_diag.SimpleDialog(
                title="Polynomial Interpolation",
                text=message,
                buttons=["OK"],
                master=self,
                cancel=0,
                default=0,
            )
            dsimple.go()
            dsimple.wm_delete_window()

            shouldSave = simple_diag.SimpleDialog(
                master=self,
                text="Would you like to save the polynomial to disk",
                title="Save or Not",
                buttons=["Save", "Don't Save"],
                default=1,
                cancel=1,
            )

            opt = shouldSave.go()
            dsimple.wm_delete_window()
            if opt == 0:
                try:
                    fname = asksaveasfilename(
                        parent=self, defaultextension=".polynomial"
                    )
                    if fname is None:
                        raise Exception("No Name Given")
                    numpy_io.saveArrays(fname, karray=data)
                except Exception:
                    opt = simple_diag.SimpleDialog(
                        master=self, text="Failed to save Polynomial ", title="Error"
                    )
            return

        return __inner_func

    def callInterpolate(self):
        try:
            c, xopt, yopt, XYOpt, *funcs = errors.InterpolateGrid_fastest(
                self.Grid_obj,
                self.Xs[0],
                self.Ys[0],
                self.Xs[1],
                self.Ys[1],
                self.dy,
                self.dx,
                savefunc=True,
                Xs=self.Xs,
                Ys=self.Ys,
            )

            region_text = f"""Region = ({self.Xs[0], self.Ys[0]})=>\
            ({self.Xs[1], self.Ys[1]})"""
            message = f"""c={c}\nxPoly={xopt}\n\
            Ypoly={yopt}\nXYPoly={XYOpt}\n{region_text}"""
            # Schedule the message box on the main thread
            while True:
                try:
                    self.jobqueue.put_nowait(
                        self.showAndOfferSavePolyNomial(
                            message,
                            xopt=xopt,
                            yopt=yopt,
                            XYOpt=XYOpt,
                            Xs=self.Xs,
                            Ys=self.Ys,
                        )
                    )
                    break
                except Full:
                    pass
        finally:
            self.jobRunning = False
            self.job = None
        return

    def callInterpolateSubView(self):
        try:
            c, xopt, yopt, XYOpt, *funcs = errors.InterpolateGrid_fastest(
                self.zoomedArea,
                self.zoomedXs[0],
                self.zoomedYs[0],
                self.zoomedXs[1],
                self.zoomedYs[1],
                self.dy,
                self.dx,
                savefunc=True,
                Xs=self.zoomedXs,
                Ys=self.zoomedYs,
            )
            region_text = f"""Region=({self.zoomedXs[0], self.zoomedYs[0]})=>
            ({self.zoomedXs[1], self.zoomedYs[1]})"""

            message = f"c={c}\nxPoly={xopt}\n\
            Ypoly={yopt}\nXYPoly={XYOpt}\n{region_text}"

            # Schedule the message box on the main thread
            while True:
                try:
                    self.jobqueue.put_nowait(
                        self.showAndOfferSavePolyNomial(
                            message,
                            xopt=xopt,
                            yopt=yopt,
                            XYOpt=XYOpt,
                            Xs=self.zoomedXs,
                            Ys=self.zoomedYs,
                        )
                    )
                    break
                except Full:
                    pass

        finally:
            self.jobRunning = False
            self.job = None
        return

    def callInterpolateSplines(self, m, n):

        try:
            height = self.Grid_obj.shape[0]
            width = self.Grid_obj.shape[1]
            leftoversheight = height % m
            leftoverswidth = width % n
            subviews = np.array(
                np.split(self.Grid_obj[:, : (-leftoverswidth or None)], n, -1)
            )
            subviews_real = np.array(
                np.split(subviews[: (-leftoversheight or None), :], m, -2)
            )
            print(subviews_real)
            c, xopt, yopt, XYOpt, *funcs = errors.InterpolateGrid_fastest(
                self.Grid_obj,
                self.Xs[0],
                self.Ys[0],
                self.Xs[1],
                self.Ys[1],
                self.dy,
                self.dx,
                savefunc=True,
                Xs=self.Xs,
                Ys=self.Ys,
            )

            region_text = (
                f"Region = ({self.Xs[0], self.Ys[0]})=>({self.Xs[1], self.Ys[1]})"
            )
            message = (
                f"c={c}\nxPoly={xopt}\nYpoly={yopt}\nXYPoly={XYOpt}\n{region_text}"
            )
            # Schedule the message box on the main thread
            while True:
                try:
                    self.jobqueue.put_nowait(
                        self.showAndOfferSavePolyNomial(
                            message,
                            xopt=xopt,
                            yopt=yopt,
                            XYOpt=XYOpt,
                            Xs=self.Xs,
                            Ys=self.Ys,
                        )
                    )
                    break
                except Full:
                    pass
        finally:
            self.jobRunning = False
            self.job = None
        return

    def calculatePolyNomial(self):
        if self.jobRunning:
            msgbox.showwarning(
                message="You Must Wait till the last job Finishes Before creating a new one",
                title="Warning",
            )
            return
        diag = simple_diag.SimpleDialog(
            self,
            "Would you like to calulate polyNomial\nOn The Full Grid or zoomed subsection?",
            ["FullGrid", "Subsection", "Cancel"],
            1,
            2,
            "Error PolyNomial",
        )
        opt = diag.go()
        self.jobRunning = True
        match opt:
            case 0:
                self.job = Thread(
                    target=self.callInterpolate, name="Full Grid Interpolate"
                )
                self.job.start()
            case 1:
                self.job = Thread(
                    target=self.callInterpolateSubView, name="SubView Interpolate"
                )
                self.job.start()
            case _:
                self.jobRunning = False

    def findLaplacian(self):

        smdiag = simple_diag.SimpleDialog(
            self,
            text="What would you like to take the laplacian of?",
            buttons=["Full Area", "Zoomed Area"],
            default=0,
            cancel=0,
            title="Laplacian",
        )
        opt = smdiag.go()
        match opt:
            case 1:
                grd = self.zoomedArea

            case _:
                grd = self.Grid_obj

        smdiag = simple_diag.SimpleDialog(
            self,
            text="Would you like to wrap the sides",
            buttons=["No", "Only_X", "Only_Y", "Both"],
            default=0,
            cancel=0,
            title="Wrapping",
        )
        opt = smdiag.go()
        match opt:

            case 1:
                lastfield = (True, "x")
            case 2:
                lastfield = (True, "y")
            case 3:
                lastfield = (True, "both")
            case _:
                lastfield = (False, "none")

        error, abserr = errors.laplaceify(
            grid=grd,
            dx=self.dx,
            dy=self.dy,
            wrap=lastfield[0],
            wrap_direction=lastfield[1],
        )

        absroot = tk.Toplevel(self)
        errroot = tk.Toplevel(self)

        absframe = InspectFrame(
            absroot,
            abserr,
            self.dx,
            self.dy,
            title="ABS residuals Laplacian",
            xlabel="X label",
            ylabel="Y label",
        )

        absframe.pack()

        errframe = InspectFrame(
            errroot,
            error,
            self.dx,
            self.dy,
            title="Residuals Laplacian",
            xlabel="X label",
            ylabel="Y label",
        )
        errframe.pack()


if __name__ == "__main__":

    grid = np.full((10, 10), fill_value=1)
    grid[(0, -1), :] = grid[:, (0, -1)] = 9
    newErrorWindow = tk.Tk()
    iframe = InspectFrame(newErrorWindow, grid, 1, 1)
    iframe.pack()
    newErrorWindow.mainloop()
