from app.ui.main_window import MainWindow
import customtkinter as ctk

if __name__ == "__main__":
    # Set appearance mode
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    # Start Application
    app = MainWindow()
    app.mainloop()
