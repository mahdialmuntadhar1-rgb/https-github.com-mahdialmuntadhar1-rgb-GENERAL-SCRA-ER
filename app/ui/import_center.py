import customtkinter as ctk
from tkinter import filedialog
from app.services.import_service import ImportService
import logging

class ImportCenterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.import_service = ImportService()

        self.label = ctk.CTkLabel(self, text="Import Center", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.import_btn = ctk.CTkButton(self, text="Select File (CSV, Excel, JSON)", command=self.select_file)
        self.import_btn.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="No file selected")
        self.status_label.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Data Files", "*.csv *.xlsx *.xls *.json")]
        )
        if file_path:
            self.status_label.configure(text=f"Importing: {file_path.split('/')[-1]}...")
            try:
                batch_id = self.import_service.import_from_file(file_path)
                self.status_label.configure(text=f"Success! Batch ID: {batch_id}")
                self.controller.frames["Dashboard"].update_stats()
            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}")
                logging.error(f"Import error: {str(e)}")
