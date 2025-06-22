"""
SyEI - Holistic Medical Center SQLAlchemy Models
Python SQLAlchemy models for the medical center backoffice system
"""

from datetime import datetime, date, time
from typing import Optional, List
from sqlalchemy import (
    Column, String, DateTime, Boolean, Text, Integer, 
    ForeignKey, UniqueConstraint, CheckConstraint, JSON
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

def generate_uuid():
    """Generate a UUID for primary keys"""
    return str(uuid.uuid4())

# =====================================================
# CORE MODELS
# =====================================================

class User(Base):
    """User model - Base user accounts with role-based access"""
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # Admin, Specialist, Patient, FamilyMember
    registration_date = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    specialist = relationship("Specialist", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)
    family_member = relationship("FamilyMember", back_populates="user", uselist=False)
    
    # Audit relationships
    created_user = relationship("User", foreign_keys=[created_by], remote_side=[id])
    updated_user = relationship("User", foreign_keys=[updated_by], remote_side=[id])
    
    # Notifications
    notifications = relationship("Notification", back_populates="user")
    
    # Audit logs
    audit_logs = relationship("AuditLog", back_populates="user")
    
    __table_args__ = (
        CheckConstraint(
            role.in_(['Admin', 'Specialist', 'Patient', 'FamilyMember']),
            name='valid_user_role'
        ),
    )

class Specialist(Base):
    """Specialist model - Medical professionals with specialties"""
    __tablename__ = 'specialists'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    specialty = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    phone_number = Column(String(20), nullable=True)
    professional_license = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="specialist")
    appointments = relationship("Appointment", back_populates="specialist")
    availability_blocks = relationship("AvailabilityBlock", back_populates="specialist")
    medical_records = relationship("MedicalRecord", back_populates="specialist")
    templates = relationship("Template", back_populates="specialist")
    educational_materials = relationship("EducationalMaterial", back_populates="specialist")
    
    # Audit relationships
    created_user = relationship("User", foreign_keys=[created_by])
    updated_user = relationship("User", foreign_keys=[updated_by])

class Patient(Base):
    """Patient model - Patient profiles and medical information"""
    __tablename__ = 'patients'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    address = Column(Text, nullable=True)
    emergency_phone = Column(String(20), nullable=True)
    emergency_contact_name = Column(String(200), nullable=True)
    base_medical_history = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="patient")
    family_members = relationship("FamilyMember", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
    medical_records = relationship("MedicalRecord", back_populates="patient")
    material_assignments = relationship("PatientMaterialAssignment", back_populates="patient")
    
    # Audit relationships
    created_user = relationship("User", foreign_keys=[created_by])
    updated_user = relationship("User", foreign_keys=[updated_by])

class FamilyMember(Base):
    """Family Member model - Family relationships and access"""
    __tablename__ = 'family_members'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    relationship = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="family_member")
    patient = relationship("Patient", back_populates="family_members")
    
    # Audit relationships
    created_user = relationship("User", foreign_keys=[created_by])
    updated_user = relationship("User", foreign_keys=[updated_by])
    
    __table_args__ = (
        UniqueConstraint('user_id', 'patient_id', name='unique_user_patient'),
    )

# =====================================================
# APPOINTMENT AND CALENDAR MANAGEMENT MODELS
# =====================================================

class Appointment(Base):
    """Appointment model - Scheduling and appointment tracking"""
    __tablename__ = 'appointments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    specialist_id = Column(UUID(as_uuid=True), ForeignKey('specialists.id', ondelete='CASCADE'), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    status = Column(String(20), default='Pending', nullable=False)
    appointment_type = Column(String(50), nullable=False)
    internal_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    specialist = relationship("Specialist", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    
    # Audit relationships
    created_user = relationship("User", foreign_keys=[created_by])
    updated_user = relationship("User", foreign_keys=[updated_by])
    
    __table_args__ = (
        CheckConstraint(
            status.in_(['Pending', 'Confirmed', 'Canceled', 'Completed', 'NoShow']),
            name='valid_appointment_status'
        ),
        CheckConstraint(
            end_datetime > start_datetime,
            name='valid_appointment_time'
        ),
    )

class AvailabilityBlock(Base):
    """Availability Block model - Specialist availability management"""
    __tablename__ = 'availability_blocks'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    specialist_id = Column(UUID(as_uuid=True), ForeignKey('specialists.id', ondelete='CASCADE'), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 1=Monday, 7=Sunday
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    exception_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    specialist = relationship("Specialist", back_populates="availability_blocks")
    
    # Audit relationships
    created_user = relationship("User", foreign_keys=[created_by])
    updated_user = relationship("User", foreign_keys=[updated_by])
    
    __table_args__ = (
        CheckConstraint(
            day_of_week >= 1 and day_of_week <= 7,
            name='valid_day_of_week'
        ),
        CheckConstraint(
            end_time > start_time,
            name='valid_time_range'
        ),
    )

# =====================================================
# MEDICAL RECORDS AND CONTENT MODELS
# =====================================================

class MedicalRecord(Base):
    """Medical Record model - Patient medical history and treatments"""
    __tablename__ = 'medical_records'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    specialist_id = Column(UUID(as_uuid=True), ForeignKey('specialists.id', ondelete='CASCADE'), nullable=False)
    record_date = Column(DateTime, default=func.now(), nullable=False)
    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    progress_notes = Column(Text, nullable=True)
    attached_files_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="medical_records")
    specialist = relationship("Specialist", back_populates="medical_records")
    
    # Audit relationships
    created_user = relationship("User", foreign_keys=[created_by])
    updated_user = relationship("User", foreign_keys=[updated_by])

class Template(Base):
    """Template model - Reusable medical document templates"""
    __tablename__ = 'templates'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    specialist_id = Column(UUID(as_uuid=True), ForeignKey('specialists.id', ondelete='SET NULL'), nullable=True)
    template_name = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    template_type = Column(String(50), nullable=False)
    is_global = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    specialist = relationship("Specialist", back_populates="templates")
    
    # Audit relationships
    created_user = relationship("User", foreign_keys=[created_by])
    updated_user = relationship("User", foreign_keys=[updated_by])

class EducationalMaterial(Base):
    """Educational Material model - Educational content management"""
    __tablename__ = 'educational_materials'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    content_url = Column(Text, nullable=False)
    material_type = Column(String(50), nullable=False)
    publish_date = Column(DateTime, default=func.now())
    specialist_id = Column(UUID(as_uuid=True), ForeignKey('specialists.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    specialist = relationship("Specialist", back_populates="educational_materials")
    material_assignments = relationship("PatientMaterialAssignment", back_populates="material")
    
    # Audit relationships
    created_user = relationship("User", foreign_keys=[created_by])
    updated_user = relationship("User", foreign_keys=[updated_by])

class PatientMaterialAssignment(Base):
    """Patient Material Assignment model - Patient-specific content assignments"""
    __tablename__ = 'patient_material_assignments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    material_id = Column(UUID(as_uuid=True), ForeignKey('educational_materials.id', ondelete='CASCADE'), nullable=False)
    assignment_date = Column(DateTime, default=func.now(), nullable=False)
    specialist_comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="material_assignments")
    material = relationship("EducationalMaterial", back_populates="material_assignments")
    
    # Audit relationships
    created_user = relationship("User", foreign_keys=[created_by])
    updated_user = relationship("User", foreign_keys=[updated_by])
    
    __table_args__ = (
        UniqueConstraint('patient_id', 'material_id', name='unique_patient_material'),
    )

# =====================================================
# ADDITIONAL MODELS FOR AUDIT & PERMISSIONS
# =====================================================

class Notification(Base):
    """Notification model - System notifications management"""
    __tablename__ = 'notifications'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")

class AuditLog(Base):
    """Audit Log model - Track changes to sensitive data"""
    __tablename__ = 'audit_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    table_name = Column(String(100), nullable=False)
    record_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String(20), nullable=False)  # INSERT, UPDATE, DELETE
    old_values = Column(JSONB, nullable=True)
    new_values = Column(JSONB, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    timestamp = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    __table_args__ = (
        CheckConstraint(
            action.in_(['INSERT', 'UPDATE', 'DELETE']),
            name='valid_audit_action'
        ),
    )

# =====================================================
# ENUMS (Python Enums for type safety)
# =====================================================

from enum import Enum

class UserRole(Enum):
    ADMIN = "Admin"
    SPECIALIST = "Specialist"
    PATIENT = "Patient"
    FAMILY_MEMBER = "FamilyMember"

class AppointmentStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELED = "Canceled"
    COMPLETED = "Completed"
    NO_SHOW = "NoShow"

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def create_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(engine)

def drop_tables(engine):
    """Drop all tables from the database"""
    Base.metadata.drop_all(engine)

# =====================================================
# SAMPLE DATA CREATION
# =====================================================

def create_sample_data(session):
    """Create sample data for development/testing"""
    from werkzeug.security import generate_password_hash
    
    # Create admin user
    admin_user = User(
        first_name="Admin",
        last_name="User",
        email="admin@medicalcenter.com",
        password_hash=generate_password_hash("admin123"),
        role="Admin"
    )
    session.add(admin_user)
    
    # Create specialist user
    specialist_user = User(
        first_name="Dr. Sarah",
        last_name="Johnson",
        email="sarah.johnson@medicalcenter.com",
        password_hash=generate_password_hash("specialist123"),
        role="Specialist"
    )
    session.add(specialist_user)
    
    # Create patient user
    patient_user = User(
        first_name="John",
        last_name="Doe",
        email="john.doe@email.com",
        password_hash=generate_password_hash("patient123"),
        role="Patient"
    )
    session.add(patient_user)
    
    session.commit()
    
    # Create specialist profile
    specialist = Specialist(
        user_id=specialist_user.id,
        specialty="Acupuncture",
        description="Licensed acupuncturist with 10+ years of experience",
        phone_number="+1-555-0123",
        professional_license="ACU-12345",
        bio="Dr. Sarah Johnson is a certified acupuncturist specializing in pain management and stress relief."
    )
    session.add(specialist)
    
    # Create patient profile
    patient = Patient(
        user_id=patient_user.id,
        date_of_birth=datetime(1985, 6, 15),
        address="123 Main St, City, State 12345",
        emergency_phone="+1-555-9999",
        emergency_contact_name="Jane Doe",
        base_medical_history="No known allergies. Previous treatments include physical therapy for back pain."
    )
    session.add(patient)
    
    session.commit() 