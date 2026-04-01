import re
from typing import Dict, List, Any, Optional

class DataValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        if not email: return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        # Simple Iraq phone validation (e.g., 07701234567 or +9647701234567)
        if not phone: return False
        pattern = r'^(\+964|0)?7[0-9]{9}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def validate_url(url: str) -> bool:
        if not url: return False
        pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        return bool(re.match(pattern, url))

    @staticmethod
    def check_university(data: Dict[str, Any]) -> List[str]:
        errors = []
        if not data.get("name_ar"):
            errors.append("Arabic Name is required")
        
        website = data.get("website_url")
        if website and not DataValidator.validate_url(website):
            errors.append("Invalid Website URL")
            
        return errors
