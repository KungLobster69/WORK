import tkinter as tk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__() # สร้างหน้าต่างหลัก
        self.title("My OOP GUI")
        self.geometry("300x200")
        
        # วางโครงสร้าง UI
        self.create_widgets()

    def create_widgets(self):
        # สร้าง Widget และเก็บไว้ใน self
        self.label = tk.Label(self, text="Hello OOP GUI!", font=("Arial", 14))
        self.label.pack(pady=20)
        
        self.btn = tk.Button(self, text="Click Me", command=self.on_click)
        self.btn.pack(pady=10)
        
    def on_click(self):
        self.label.config(text="Button Clicked!", fg="red")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()