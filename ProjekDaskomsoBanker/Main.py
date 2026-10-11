import tkinter as tk
from BankerGUI import BankerGUI

def main():
    root = tk.Tk()
    # Menjalankan aplikasi dengan melemparkan objek root ke BankerGUI
    app = BankerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()