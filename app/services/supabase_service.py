import os
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseService:
    def __init__(self):
        url: str = os.getenv("SUPABASE_URL", "")
        # Prefer service role key for admin app if available, otherwise use anon key
        key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY", "")
        if not url or not key:
            print("Warning: SUPABASE_URL or SUPABASE_KEY not found in .env")
        self.client: Client = create_client(url, key)

    # --- Universities ---
    def get_universities(self) -> List[Dict[str, Any]]:
        response = self.client.table("universities").select("*").order("name_ar").execute()
        return response.data

    def create_university(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self.client.table("universities").insert(data).execute()
        return response.data[0] if response.data else {}

    def update_university(self, university_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self.client.table("universities").update(data).eq("id", university_id).execute()
        return response.data[0] if response.data else {}

    # --- Staging ---
    def get_staging_records(self, status: str = "pending") -> List[Dict[str, Any]]:
        response = self.client.table("staging_records").select("*").eq("status", status).execute()
        return response.data

    def create_staging_record(self, raw_data: Dict[str, Any], source_file: str = "manual") -> Dict[str, Any]:
        data = {
            "raw_data": raw_data,
            "source_file": source_file,
            "status": "pending"
        }
        response = self.client.table("staging_records").insert(data).execute()
        return response.data[0] if response.data else {}

    def update_staging_status(self, record_id: str, status: str, errors: Optional[Dict] = None) -> Dict[str, Any]:
        update_data = {"status": status}
        if errors:
            update_data["validation_errors"] = errors
        response = self.client.table("staging_records").update(update_data).eq("id", record_id).execute()
        return response.data[0] if response.data else {}

    # --- Governorates & Cities ---
    def get_governorates(self) -> List[Dict[str, Any]]:
        response = self.client.table("governorates").select("*").execute()
        return response.data

    def get_cities(self, governorate_id: Optional[str] = None) -> List[Dict[str, Any]]:
        query = self.client.table("cities").select("*")
        if governorate_id:
            query = query.eq("governorate_id", governorate_id)
        response = query.execute()
        return response.data
