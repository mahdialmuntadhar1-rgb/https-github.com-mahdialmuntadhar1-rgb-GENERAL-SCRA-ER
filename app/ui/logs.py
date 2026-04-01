import customtkinter as ctk
from app.database.session import SessionLocal
from app.models.staging import SyncLog

class LogsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="System Logs", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Activity History")
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_btn = ctk.CTkButton(self, text="Refresh Logs", command=self.load_logs)
        self.refresh_btn.pack(pady=10)

        self.load_logs()

    def load_logs(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        db = SessionLocal()
        try:
            logs = db.query(SyncLog).order_by(SyncLog.created_at.desc()).limit(50).all()
            for log in logs:
                row = ctk.CTkFrame(self.scrollable_frame)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=f"[{log.created_at}] {log.action}: {log.status}").pack(side="left", padx=10)
        finally:
            db.close()
