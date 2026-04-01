import pandas as pd
import json
from typing import List, Dict, Any
from .supabase_service import SupabaseService

class ImportService:
    def __init__(self, supabase_service: SupabaseService):
        self.supabase = supabase_service

    def import_csv(self, file_path: str) -> int:
        df = pd.read_csv(file_path)
        return self._process_dataframe(df, file_path)

    def import_excel(self, file_path: str) -> int:
        df = pd.read_excel(file_path)
        return self._process_dataframe(df, file_path)

    def import_json(self, file_path: str) -> int:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            count = 0
            for item in data:
                self.supabase.create_staging_record(item, file_path)
                count += 1
            return count
        return 0

    def _process_dataframe(self, df: pd.DataFrame, source: str) -> int:
        # Convert NaN to None for JSON compatibility
        df = df.where(pd.notnull(df), None)
        records = df.to_dict('records')
        
        count = 0
        for record in records:
            self.supabase.create_staging_record(record, source)
            count += 1
        return count
