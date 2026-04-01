import pandas as pd
import json
from app.database.session import SessionLocal
from app.models.staging import University, RecordStatus
import os

class ExportService:
    def __init__(self):
        self.db = SessionLocal()

    def export_approved_universities(self, format: str = "csv"):
        unis = self.db.query(University).filter(University.status == RecordStatus.APPROVED.value).all()
        data = []
        for u in unis:
            data.append({
                "id": u.id,
                "name_en": u.name_en,
                "name_ar": u.name_ar,
                "website": u.website,
                "status": u.status
            })
        
        df = pd.DataFrame(data)
        os.makedirs("exports", exist_ok=True)
        
        file_path = f"exports/approved_universities.{format}"
        if format == "csv":
            df.to_csv(file_path, index=False)
        elif format == "json":
            df.to_json(file_path, orient="records", indent=4)
        
        self.db.close()
        return file_path
