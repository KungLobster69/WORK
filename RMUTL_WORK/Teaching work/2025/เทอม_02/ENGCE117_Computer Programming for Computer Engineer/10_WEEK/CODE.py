import tkinter as tk

root = tk.Tk()
root.geometry("200x150")

# จัดเรียงจากบนลงล่าง และให้ขยายเต็มแกน X แนวนอน
tk.Button(root, text="Top Button", bg="red", fg="white").pack(side=tk.TOP, fill=tk.X)
tk.Button(root, text="Bottom Button", bg="blue", fg="white").pack(side=tk.BOTTOM, fill=tk.X)

# จัดเรียงซ้ายขวา
tk.Button(root, text="Left", bg="green", fg="white").pack(side=tk.LEFT, fill=tk.Y)
tk.Button(root, text="Right", bg="orange", fg="black").pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()