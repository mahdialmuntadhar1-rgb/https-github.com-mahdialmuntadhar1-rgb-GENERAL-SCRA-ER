import customtkinter as ctk
from app.services.export_service import ExportService
import os

class ExportsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.export_service = ExportService()

        self.label = ctk.CTkLabel(self, text="Export Center", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.csv_btn = ctk.CTkButton(self, text="Export Approved Universities (CSV)", command=lambda: self.export("csv"))
        self.csv_btn.pack(pady=10)

        self.json_btn = ctk.CTkButton(self, text="Export Approved Universities (JSON)", command=lambda: self.export("json"))
        self.json_btn.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Select export format")
        self.status_label.pack(pady=20)

    def export(self, format):
        try:
            path = self.export_service.export_approved_universities(format)
            self.status_label.configure(text=f"Exported to: {os.path.abspath(path)}")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
