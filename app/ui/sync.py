import customtkinter as ctk
from app.services.sync_service import SyncService

class SyncFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sync_service = SyncService()

        self.label = ctk.CTkLabel(self, text="Sync Center", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.info = ctk.CTkLabel(self, text="Sync approved data to Supabase production database.")
        self.info.pack(pady=10)

        self.sync_btn = ctk.CTkButton(self, text="Start Sync to Supabase", command=self.run_sync)
        self.sync_btn.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Ready to sync")
        self.status_label.pack(pady=10)

    def run_sync(self):
        self.status_label.configure(text="Syncing...")
        success = self.sync_service.sync_to_supabase()
        if success:
            self.status_label.configure(text="Sync completed successfully!")
        else:
            self.status_label.configure(text="Sync failed. Check logs.")
