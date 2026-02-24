import tkinter as tk

def on_click():
    print("Button Clicked!")

root = tk.Tk()
btn = tk.Button(root, text="Click Me", command=on_click)
btn.pack()

root.mainloop()