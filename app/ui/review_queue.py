import customtkinter as ctk
from app.database.session import SessionLocal
from app.models.staging import RawRecord
import json

class ReviewQueueFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Review Queue", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Pending Records")
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_btn = ctk.CTkButton(self, text="Refresh", command=self.load_records)
        self.refresh_btn.pack(pady=10)

        self.load_records()

    def load_records(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        db = SessionLocal()
        try:
            records = db.query(RawRecord).filter(RawRecord.status == "raw").limit(20).all()
            for rec in records:
                data = json.loads(rec.source_data)
                name = data.get("name_en", "Unknown")
                
                row = ctk.CTkFrame(self.scrollable_frame)
                row.pack(fill="x", pady=5)
                
                ctk.CTkLabel(row, text=f"ID: {rec.id} | {name}").pack(side="left", padx=10)
                ctk.CTkButton(row, text="Approve", width=60, command=lambda r=rec: self.approve_record(r)).pack(side="right", padx=5)
                ctk.CTkButton(row, text="Reject", width=60, fg_color="red", command=lambda r=rec: self.reject_record(r)).pack(side="right", padx=5)
        finally:
            db.close()

    def approve_record(self, record):
        db = SessionLocal()
        try:
            rec = db.query(RawRecord).get(record.id)
            data = json.loads(rec.source_data)
            
            # Create production-ready University record
            new_uni = University(
                name_en=data.get("name_en"),
                name_ar=data.get("name_ar"),
                website=data.get("website"),
                address=data.get("address"),
                institution_type=data.get("institution_type", "University"),
                public_private=data.get("public_private", "Public"),
                status="approved",
                governorate_id=1, # Default for MVP
                city_id=1        # Default for MVP
            )
            db.add(new_uni)
            rec.status = "approved"
            db.commit()
            self.load_records()
            if "Dashboard" in self.controller.frames:
                self.controller.frames["Dashboard"].update_stats()
        except Exception as e:
            print(f"Error approving record: {e}")
            db.rollback()
        finally:
            db.close()

    def reject_record(self, record):
        db = SessionLocal()
        try:
            rec = db.query(RawRecord).get(record.id)
            rec.status = "rejected"
            db.commit()
            self.load_records()
        finally:
            db.close()
