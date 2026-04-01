import customtkinter as ctk
from app.services.validation_service import ValidationService

class ValidationCenterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.validation_service = ValidationService()

        self.label = ctk.CTkLabel(self, text="Validation Center", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.run_btn = ctk.CTkButton(self, text="Run Validation Engine", command=self.run_validation)
        self.run_btn.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Ready to validate records")
        self.status_label.pack(pady=10)

    def run_validation(self):
        self.status_label.configure(text="Validating...")
        count = self.validation_service.validate_raw_records()
        self.status_label.configure(text=f"Validation complete. Processed {count} records.")
        self.controller.frames["Dashboard"].update_stats()
