-- SyEI - Holistic Medical Center Database Schema
-- This file contains all the database tables for the medical center backoffice system

-- Enable UUID extension for PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- CORE TABLES
-- =====================================================

-- Users table - Base user accounts with role-based access
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Admin', 'Specialist', 'Patient', 'FamilyMember')),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID
);

-- Specialists table - Medical professionals with specialties
CREATE TABLE specialists (
    specialist_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    specialty VARCHAR(100) NOT NULL,
    description TEXT,
    phone_number VARCHAR(20),
    professional_license VARCHAR(100),
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    UNIQUE(user_id)
);

-- Patients table - Patient profiles and medical information
CREATE TABLE patients (
    patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    date_of_birth DATE NOT NULL,
    address TEXT,
    emergency_phone VARCHAR(20),
    emergency_contact_name VARCHAR(200),
    base_medical_history TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    UNIQUE(user_id)
);

-- Family Members table - Family relationships and access
CREATE TABLE family_members (
    family_member_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    patient_id UUID NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    relationship VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    UNIQUE(user_id, patient_id)
);

-- =====================================================
-- APPOINTMENT AND CALENDAR MANAGEMENT TABLES
-- =====================================================

-- Appointments table - Scheduling and appointment tracking
CREATE TABLE appointments (
    appointment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    specialist_id UUID NOT NULL REFERENCES specialists(specialist_id) ON DELETE CASCADE,
    patient_id UUID NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Confirmed', 'Canceled', 'Completed', 'NoShow')),
    appointment_type VARCHAR(50) NOT NULL,
    internal_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    CONSTRAINT valid_appointment_time CHECK (end_datetime > start_datetime)
);

-- Availability Blocks table - Specialist availability management
CREATE TABLE availability_blocks (
    availability_block_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    specialist_id UUID NOT NULL REFERENCES specialists(specialist_id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 7), -- 1=Monday, 7=Sunday
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    exception_date DATE, -- For specific days that override day_of_week
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    CONSTRAINT valid_time_range CHECK (end_time > start_time)
);

-- =====================================================
-- MEDICAL RECORDS AND CONTENT TABLES
-- =====================================================

-- Medical Records table - Patient medical history and treatments
CREATE TABLE medical_records (
    record_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    specialist_id UUID NOT NULL REFERENCES specialists(specialist_id) ON DELETE CASCADE,
    record_date DATE NOT NULL DEFAULT CURRENT_DATE,
    diagnosis TEXT,
    treatment TEXT,
    progress_notes TEXT,
    attached_files_json JSONB, -- Store paths to files like PDFs, images
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID
);

-- Templates table - Reusable medical document templates
CREATE TABLE templates (
    template_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    specialist_id UUID REFERENCES specialists(specialist_id) ON DELETE SET NULL, -- NULL for global templates
    template_name VARCHAR(200) NOT NULL,
    content TEXT NOT NULL, -- Can be HTML or Markdown
    template_type VARCHAR(50) NOT NULL, -- e.g., Initial Diagnosis, Follow-up, Report
    is_global BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID
);

-- Educational Materials table - Educational content management
CREATE TABLE educational_materials (
    material_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    content_url TEXT NOT NULL, -- Link to video, externally hosted PDF, or internal path
    material_type VARCHAR(50) NOT NULL, -- e.g., Video, PDF, Article, Infographic
    publish_date DATE DEFAULT CURRENT_DATE,
    specialist_id UUID REFERENCES specialists(specialist_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID
);

-- Patient Material Assignments table - Patient-specific content assignments
CREATE TABLE patient_material_assignments (
    assignment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    material_id UUID NOT NULL REFERENCES educational_materials(material_id) ON DELETE CASCADE,
    assignment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    specialist_comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID,
    updated_by UUID,
    UNIQUE(patient_id, material_id)
);

-- =====================================================
-- ADDITIONAL TABLES FOR AUDIT & PERMISSIONS
-- =====================================================

-- Notifications table - System notifications management
CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL, -- e.g., Appointment, Material, System
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP
);

-- Audit Log table - Track changes to sensitive data
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL, -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    user_id UUID REFERENCES users(user_id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active);

-- Specialists indexes
CREATE INDEX idx_specialists_user_id ON specialists(user_id);
CREATE INDEX idx_specialists_specialty ON specialists(specialty);

-- Patients indexes
CREATE INDEX idx_patients_user_id ON patients(user_id);
CREATE INDEX idx_patients_dob ON patients(date_of_birth);

-- Family Members indexes
CREATE INDEX idx_family_members_user_id ON family_members(user_id);
CREATE INDEX idx_family_members_patient_id ON family_members(patient_id);

-- Appointments indexes
CREATE INDEX idx_appointments_specialist_id ON appointments(specialist_id);
CREATE INDEX idx_appointments_patient_id ON appointments(patient_id);
CREATE INDEX idx_appointments_start_datetime ON appointments(start_datetime);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_date_range ON appointments(start_datetime, end_datetime);

-- Availability Blocks indexes
CREATE INDEX idx_availability_blocks_specialist_id ON availability_blocks(specialist_id);
CREATE INDEX idx_availability_blocks_day_time ON availability_blocks(day_of_week, start_time, end_time);
CREATE INDEX idx_availability_blocks_exception_date ON availability_blocks(exception_date);

-- Medical Records indexes
CREATE INDEX idx_medical_records_patient_id ON medical_records(patient_id);
CREATE INDEX idx_medical_records_specialist_id ON medical_records(specialist_id);
CREATE INDEX idx_medical_records_date ON medical_records(record_date);

-- Templates indexes
CREATE INDEX idx_templates_specialist_id ON templates(specialist_id);
CREATE INDEX idx_templates_type ON templates(template_type);
CREATE INDEX idx_templates_global ON templates(is_global);

-- Educational Materials indexes
CREATE INDEX idx_educational_materials_type ON educational_materials(material_type);
CREATE INDEX idx_educational_materials_specialist_id ON educational_materials(specialist_id);
CREATE INDEX idx_educational_materials_publish_date ON educational_materials(publish_date);

-- Patient Material Assignments indexes
CREATE INDEX idx_patient_material_assignments_patient_id ON patient_material_assignments(patient_id);
CREATE INDEX idx_patient_material_assignments_material_id ON patient_material_assignments(material_id);
CREATE INDEX idx_patient_material_assignments_date ON patient_material_assignments(assignment_date);

-- Notifications indexes
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);

-- Audit Log indexes
CREATE INDEX idx_audit_logs_table_record ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);

-- =====================================================
-- TRIGGERS FOR AUDIT LOGGING
-- =====================================================

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at trigger to all tables with updated_at column
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_specialists_updated_at BEFORE UPDATE ON specialists FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_family_members_updated_at BEFORE UPDATE ON family_members FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_availability_blocks_updated_at BEFORE UPDATE ON availability_blocks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_medical_records_updated_at BEFORE UPDATE ON medical_records FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_templates_updated_at BEFORE UPDATE ON templates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_educational_materials_updated_at BEFORE UPDATE ON educational_materials FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_patient_material_assignments_updated_at BEFORE UPDATE ON patient_material_assignments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- SAMPLE DATA (Optional - for development/testing)
-- =====================================================

-- Insert sample admin user (password: admin123)
INSERT INTO users (user_id, first_name, last_name, email, password_hash, role) 
VALUES (
    uuid_generate_v4(), 
    'Admin', 
    'User', 
    'admin@medicalcenter.com', 
    '$2b$10$rQZ8K9mN2pL1vX3yU6wQ7eR4tY5uI8oP9aB2cD3eF4gH5iJ6kL7mN8oP9qR', 
    'Admin'
);

-- Insert sample specialist
INSERT INTO users (user_id, first_name, last_name, email, password_hash, role) 
VALUES (
    uuid_generate_v4(), 
    'Dr. Sarah', 
    'Johnson', 
    'sarah.johnson@medicalcenter.com', 
    '$2b$10$rQZ8K9mN2pL1vX3yU6wQ7eR4tY5uI8oP9aB2cD3eF4gH5iJ6kL7mN8oP9qR', 
    'Specialist'
);

-- Insert sample patient
INSERT INTO users (user_id, first_name, last_name, email, password_hash, role) 
VALUES (
    uuid_generate_v4(), 
    'John', 
    'Doe', 
    'john.doe@email.com', 
    '$2b$10$rQZ8K9mN2pL1vX3yU6wQ7eR4tY5uI8oP9aB2cD3eF4gH5iJ6kL7mN8oP9qR', 
    'Patient'
); 