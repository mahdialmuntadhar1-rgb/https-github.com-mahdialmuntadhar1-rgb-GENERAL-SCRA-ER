import customtkinter as ctk
from app.database.session import SessionLocal
from app.models.staging import University

class UniversitiesFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="University Management", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Approved Universities")
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_btn = ctk.CTkButton(self, text="Refresh List", command=self.load_universities)
        self.refresh_btn.pack(pady=10)

        self.load_universities()

    def load_universities(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        db = SessionLocal()
        try:
            unis = db.query(University).all()
            for uni in unis:
                row = ctk.CTkFrame(self.scrollable_frame)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=f"{uni.name_en} ({uni.name_ar})").pack(side="left", padx=10)
                ctk.CTkLabel(row, text=f"Status: {uni.status}", text_color="green").pack(side="right", padx=10)
        finally:
            db.close()
