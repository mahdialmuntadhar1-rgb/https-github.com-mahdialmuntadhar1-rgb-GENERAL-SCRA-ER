import customtkinter as ctk
from app.database.session import SessionLocal
from app.models.staging import University, RawRecord, ImportBatch

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.label = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.stats_container = ctk.CTkFrame(self)
        self.stats_container.pack(fill="x", padx=20, pady=10)

        self.update_stats()

    def update_stats(self):
        db = SessionLocal()
        try:
            total_raw = db.query(RawRecord).count()
            total_uni = db.query(University).count()
            total_batches = db.query(ImportBatch).count()
            needs_review = db.query(RawRecord).filter(RawRecord.status == "needs_review").count()
            validated = db.query(RawRecord).filter(RawRecord.status == "validated").count()

            self.create_stat_card("Total Raw", str(total_raw), 0, 0)
            self.create_stat_card("Validated", str(validated), 0, 1)
            self.create_stat_card("Needs Review", str(needs_review), 0, 2)
            self.create_stat_card("Approved Unis", str(total_uni), 1, 0)
            self.create_stat_card("Batches", str(total_batches), 1, 1)
        finally:
            db.close()

    def create_stat_card(self, title, value, row, col):
        card = ctk.CTkFrame(self.stats_container, width=180, height=80)
        card.grid(row=row, column=col, padx=10, pady=10)
        
        t_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12))
        t_label.pack(pady=(10, 0))
        
        v_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=20, weight="bold"))
        v_label.pack(pady=(0, 10))
