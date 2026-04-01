import customtkinter as ctk
from app.config import settings

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.db_label = ctk.CTkLabel(self, text=f"Database: {settings.DATABASE_URL}")
        self.db_label.pack(pady=10)

        self.theme_label = ctk.CTkLabel(self, text="Theme Color:")
        self.theme_label.pack(pady=(20, 0))
        
        self.theme_menu = ctk.CTkOptionMenu(self, values=["blue", "green", "dark-blue"], command=self.change_theme)
        self.theme_menu.set(settings.THEME)
        self.theme_menu.pack(pady=10)

    def change_theme(self, new_theme):
        ctk.set_default_color_theme(new_theme)
        # Note: Requires restart to apply fully in some cases
