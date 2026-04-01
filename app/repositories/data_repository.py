from sqlalchemy.orm import Session
from app.models.staging import University, RawRecord, ImportBatch, Governorate, City, UniversityContact, SocialLink, Post, Opportunity

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class UniversityRepository(BaseRepository):
    def get_all(self):
        return self.db.query(University).all()
    
    def get_by_id(self, uni_id: int):
        return self.db.query(University).filter(University.id == uni_id).first()

    def create(self, data: dict):
        obj = University(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

class RawRecordRepository(BaseRepository):
    def get_pending(self):
        return self.db.query(RawRecord).filter(RawRecord.status == "raw").all()
    
    def update_status(self, record_id: int, status: str):
        record = self.db.query(RawRecord).filter(RawRecord.id == record_id).first()
        if record:
            record.status = status
            self.db.commit()
        return record

class GovernorateRepository(BaseRepository):
    def get_all(self):
        return self.db.query(Governorate).all()

class CityRepository(BaseRepository):
    def get_by_governorate(self, gov_id: int):
        return self.db.query(City).filter(City.governorate_id == gov_id).all()
