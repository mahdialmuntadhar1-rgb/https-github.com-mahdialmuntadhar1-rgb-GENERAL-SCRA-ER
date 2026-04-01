import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback):
        super().__init__(parent, width=200, corner_radius=0)
        self.show_frame = show_frame_callback

        self.logo_label = ctk.CTkLabel(self, text="Iraq Edu Data", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.dashboard_btn = ctk.CTkButton(self, text="Dashboard", command=lambda: self.show_frame("Dashboard"))
        self.dashboard_btn.grid(row=1, column=0, padx=20, pady=5)

        self.import_btn = ctk.CTkButton(self, text="Import Center", command=lambda: self.show_frame("ImportCenter"))
        self.import_btn.grid(row=2, column=0, padx=20, pady=5)

        self.validation_btn = ctk.CTkButton(self, text="Validation Center", command=lambda: self.show_frame("ValidationCenter"))
        self.validation_btn.grid(row=3, column=0, padx=20, pady=5)

        self.review_btn = ctk.CTkButton(self, text="Review Queue", command=lambda: self.show_frame("ReviewQueue"))
        self.review_btn.grid(row=4, column=0, padx=20, pady=5)

        self.uni_btn = ctk.CTkButton(self, text="Universities", command=lambda: self.show_frame("Universities"))
        self.uni_btn.grid(row=5, column=0, padx=20, pady=5)

        self.posts_btn = ctk.CTkButton(self, text="Posts", command=lambda: self.show_frame("Posts"))
        self.posts_btn.grid(row=6, column=0, padx=20, pady=5)

        self.export_btn = ctk.CTkButton(self, text="Exports", command=lambda: self.show_frame("Exports"))
        self.export_btn.grid(row=7, column=0, padx=20, pady=5)

        self.sync_btn = ctk.CTkButton(self, text="Sync", command=lambda: self.show_frame("Sync"))
        self.sync_btn.grid(row=8, column=0, padx=20, pady=5)

        self.settings_btn = ctk.CTkButton(self, text="Settings", command=lambda: self.show_frame("Settings"))
        self.settings_btn.grid(row=9, column=0, padx=20, pady=5)

        self.logs_btn = ctk.CTkButton(self, text="Logs", command=lambda: self.show_frame("Logs"))
        self.logs_btn.grid(row=10, column=0, padx=20, pady=5)

        self.spacer = ctk.CTkLabel(self, text="")
        self.spacer.grid(row=4, column=0, pady=200)

        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
