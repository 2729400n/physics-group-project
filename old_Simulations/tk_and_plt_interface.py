import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

class ResponsivePlotApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Responsive Tkinter Plot with Tools")
        self.geometry("640x480+0+0")

        # Configure grid for responsiveness
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Label to display data value from mouse click events
        self.value_label = ttk.Label(self.main_frame, text="Click on the plot to see value")
        self.value_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Frame for plot and toolbar
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=1, column=0, sticky="nsew")
        self.plot_frame.columnconfigure(0, weight=1)
        self.plot_frame.rowconfigure(0, weight=1)

        self.create_plot()

        # Bind resize event for dynamic adjustments
        self.plot_frame.bind("<Configure>", self.on_resize)
        
        self.Grid_obj :np.ndarray=None

    def create_plot(self):
        """Creates a Matplotlib figure, embeds it, and sets up tools."""
        # Create figure and axis
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Generate some data
        self.x = np.linspace(0, 10, 100)
        self.y = np.sin(self.x)
        self.line = self.ax.imshow(np.random.rand(256, 256))
        self.fig.colorbar(self.line, ax=self.ax)

        # Plot data

        self.ax.set_title("Responsive Plot")
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.legend()

        # Embed figure into Tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")

        # Add Navigation Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame,pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, sticky="ew")

        # Connect event for mouse clicks on the canvas
        self.canvas.mpl_connect("button_press_event", self.on_click)

    def on_resize(self, event):
        """Handles frame resize event to adjust the plot size."""
        new_width = event.width / self.fig.dpi
        new_height = (event.height - self.toolbar.winfo_height()) / self.fig.dpi
        self.fig.set_size_inches(new_width, new_height)
        self.canvas.draw()

    def on_click(self, event):
        """Displays the y value for the point closest to the click."""
        if event.inaxes == self.ax:
            # Calculate closest data point index using first principles: minimize distance in x
            click_x = event.xdata
            index = (np.abs(self.x - click_x)).argmin()
            closest_x = self.x[index]
            closest_y = self.y[index]
            self.value_label.config(text=f"Clicked near x={closest_x:.2f}, y={closest_y:.2f}")

if __name__ == "__main__":
    app = ResponsivePlotApp()
    app.mainloop()
