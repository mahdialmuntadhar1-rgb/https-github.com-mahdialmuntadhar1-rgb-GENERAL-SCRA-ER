import re
import json
from app.database.session import SessionLocal
from app.models.staging import RawRecord, ValidationIssue
from app.validators.schemas import UniversityValidator, ContactValidator
from pydantic import ValidationError

class ValidationService:
    def __init__(self):
        self.db = SessionLocal()

    def validate_raw_records(self):
        records = self.db.query(RawRecord).filter(RawRecord.status == "raw").all()
        for record in records:
            issues = []
            data = json.loads(record.source_data)
            
            # Simple Email Regex
            email = data.get("email")
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                issues.append(("email", "Invalid email format", "Error"))

            # Simple Phone Regex (Iraq format)
            phone = data.get("phone")
            if phone and not re.match(r"^07[789]\d{8}$", str(phone)):
                issues.append(("phone", "Invalid Iraq phone format", "Warning"))

            # Pydantic validation for structure
            try:
                # Attempt to validate as university if it looks like one
                if "name_en" in data:
                    # We might need to mock some IDs for validation if they are missing in raw data
                    temp_data = data.copy()
                    if "governorate_id" not in temp_data: temp_data["governorate_id"] = 1
                    if "city_id" not in temp_data: temp_data["city_id"] = 1
                    if "institution_type" not in temp_data: temp_data["institution_type"] = "University"
                    if "public_private" not in temp_data: temp_data["public_private"] = "Public"
                    
                    UniversityValidator(**temp_data)
            except ValidationError as e:
                for error in e.errors():
                    issues.append((error['loc'][0], error['msg'], "Error"))

            # Save issues
            if issues:
                record.status = "needs_review"
                for field, msg, severity in issues:
                    issue = ValidationIssue(
                        record_id=record.id,
                        record_type="RawRecord",
                        issue_type=field,
                        severity=severity,
                        message=msg
                    )
                    self.db.add(issue)
            else:
                record.status = "validated"
            
            self.db.commit()
        
        self.db.close()
        return len(records)
