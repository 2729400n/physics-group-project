import tkinter as tk
import tkinter.ttk as ttk

class HomePage(ttk.Frame):
    name = 'HomePage'

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Configure grid for responsiveness
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Create Label for Welcome Text
        self.header_label = ttk.Label(self.main_frame, text="Welcome to the Electrostatic Solver GUI!", font=("Helvetica", 16),justify='center')
        self.header_label.grid(row=0, column=0, padx=5, pady=20)

        # Create Label for Description Text
        self.description_label = ttk.Label(self.main_frame, text=(
            "This graphical user interface (GUI) is designed to solve electrostatic boundary conditions. "
            "You can input various boundary conditions and the solver will compute the electrostatic field solutions."
        ), wraplength=400, justify="center")
        self.description_label.grid(row=1, column=0, padx=5, pady=20)

        # Create Button Frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, padx=5, pady=20)
        
        self.button_frame.columnconfigure(0, weight=1)

        # Create Start Button
        self.start_button = ttk.Button(self.button_frame, text="Start Solving", command=self.start_solving)
        self.start_button.grid(row=0, column=0, padx=5, pady=5,sticky='nsew')
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def start_solving(self):
        """Function to start the electrostatic solver or navigate to the solver page"""
        # This could be a method to transition to the next page of the GUI where the solver interface is.
        print("Starting the electrostatic solver...")  # Placeholder for actual transition logic

scene = HomePage

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Electrostatic Solver Home Page")
    page = HomePage(master=root)
    page.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
