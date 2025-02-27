import tkinter as tk

def on_resize(event:'tk.Event[tk.Widget]'):
    width = event.width
    height = event.height
    
    print(f"Window resized to {width}x{height}")
    print("Event Type",event)

root = tk.Tk()
root.title("Resize Event Example")

# Bind the <Configure> event to the on_resize function
root.bind("<Configure>", on_resize)
root.update()

# Create a simple label to display in the window
label = tk.Label(root, text="Resize the window and check the console!")
label.pack(expand=True)

root.mainloop()
