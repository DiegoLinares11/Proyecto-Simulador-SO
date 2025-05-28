from frontend.gui import OSSimulatorGUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = OSSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()