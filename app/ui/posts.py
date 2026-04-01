import customtkinter as ctk

class PostsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Posts & Opportunities", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.info_label = ctk.CTkLabel(self, text="Manage announcements, jobs, and student life posts.")
        self.info_label.pack(pady=10)
        
        # Placeholder for CRUD
        self.add_btn = ctk.CTkButton(self, text="Create New Post", command=lambda: print("Create Post"))
        self.add_btn.pack(pady=10)
