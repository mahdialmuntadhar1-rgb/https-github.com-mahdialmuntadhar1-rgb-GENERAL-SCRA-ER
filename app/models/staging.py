from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Enum
from sqlalchemy.sql import func
from app.database.session import Base
import enum

class RecordStatus(enum.Enum):
    RAW = "raw"
    IMPORTED = "imported"
    VALIDATED = "validated"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"

class ImportBatch(Base):
    __tablename__ = "import_batches"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_type = Column(String)
    row_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RawRecord(Base):
    __tablename__ = "raw_records"
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("import_batches.id"))
    source_data = Column(Text)  # JSON string of original row
    status = Column(String, default=RecordStatus.RAW.value)
    validation_errors = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Governorate(Base):
    __tablename__ = "governorates"
    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String, unique=True)
    name_ar = Column(String, unique=True)

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    governorate_id = Column(Integer, ForeignKey("governorates.id"))
    name_en = Column(String)
    name_ar = Column(String)

class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String)
    name_ar = Column(String)
    name_ku = Column(String, nullable=True)
    institution_type = Column(String)  # University, College, Institute
    public_private = Column(String)    # Public, Private
    governorate_id = Column(Integer, ForeignKey("governorates.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    website = Column(String)
    address = Column(Text)
    description = Column(Text)
    logo_url = Column(String)
    source_url = Column(String)
    verified = Column(Boolean, default=False)
    status = Column(String, default=RecordStatus.RAW.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UniversityContact(Base):
    __tablename__ = "university_contacts"
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    contact_type = Column(String)  # General, Admission, Support
    email = Column(String)
    phone = Column(String)
    whatsapp = Column(String)
    contact_page_url = Column(String)
    source_url = Column(String)
    verified = Column(Boolean, default=False)
    status = Column(String, default=RecordStatus.RAW.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SocialLink(Base):
    __tablename__ = "social_links"
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    platform = Column(String)  # Facebook, Instagram, LinkedIn, X
    url = Column(String)
    source_url = Column(String)
    verified = Column(Boolean, default=False)
    status = Column(String, default=RecordStatus.RAW.value)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    governorate_id = Column(Integer, ForeignKey("governorates.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    category = Column(String) # jobs, internships, my_university, announcements
    language = Column(String) # en, ar, ku
    title = Column(String)
    content = Column(Text)
    image_url = Column(String)
    source_url = Column(String)
    status = Column(String, default=RecordStatus.RAW.value)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    title = Column(String)
    description = Column(Text)
    deadline = Column(DateTime(timezone=True))
    status = Column(String, default=RecordStatus.RAW.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ValidationIssue(Base):
    __tablename__ = "validation_issues"
    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer)
    record_type = Column(String) # University, Contact, etc.
    issue_type = Column(String)
    severity = Column(String) # Error, Warning
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SyncLog(Base):
    __tablename__ = "sync_logs"
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String)
    entity_id = Column(Integer)
    action = Column(String) # Push, Update
    status = Column(String) # Success, Failed
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
