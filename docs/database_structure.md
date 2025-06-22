# SyEI - Database Structure Documentation

## Overview

This document describes the complete database structure for the Holistic Medical Center Backoffice system. The database is designed to support a comprehensive medical center with multiple user roles, appointment management, medical records, and educational content.

## Database Schema Overview

The database consists of 12 main tables organized into three categories:

### Core Tables (4 tables)
- **Users** - Base user accounts with role-based access
- **Specialists** - Medical professionals with specialties
- **Patients** - Patient profiles and medical information
- **FamilyMembers** - Family relationships and access

### Management Tables (6 tables)
- **Appointments** - Scheduling and appointment tracking
- **AvailabilityBlocks** - Specialist availability management
- **MedicalRecords** - Patient medical history and treatments
- **Templates** - Reusable medical document templates
- **EducationalMaterials** - Educational content management
- **PatientMaterialAssignments** - Patient-specific content assignments

### Support Tables (2 tables)
- **Notifications** - System notifications management
- **AuditLogs** - Track changes to sensitive data

## Detailed Table Descriptions

### 1. Users Table

**Purpose**: Central user management with role-based access control

**Key Fields**:
- `user_id` (UUID, PK) - Unique identifier
- `email` (VARCHAR(255), UNIQUE) - User's email address
- `role` (VARCHAR(20)) - User role: Admin, Specialist, Patient, FamilyMember
- `is_active` (BOOLEAN) - Account status

**Relationships**:
- One-to-one with Specialists, Patients, FamilyMembers
- Self-referencing for audit tracking (created_by, updated_by)

**Indexes**:
- `idx_users_email` - For fast email lookups
- `idx_users_role` - For role-based queries
- `idx_users_active` - For active user filtering

### 2. Specialists Table

**Purpose**: Medical professionals with their specialties and credentials

**Key Fields**:
- `specialist_id` (UUID, PK) - Unique identifier
- `user_id` (UUID, FK) - Reference to Users table
- `specialty` (VARCHAR(100)) - Medical specialty (e.g., Acupuncture, Naturopathy)
- `professional_license` (VARCHAR(100)) - License number
- `bio` (TEXT) - Professional biography

**Relationships**:
- Many-to-one with Users
- One-to-many with Appointments, AvailabilityBlocks, MedicalRecords, Templates, EducationalMaterials

**Constraints**:
- Unique constraint on `user_id` (one specialist per user)

### 3. Patients Table

**Purpose**: Patient profiles with medical and contact information

**Key Fields**:
- `patient_id` (UUID, PK) - Unique identifier
- `user_id` (UUID, FK) - Reference to Users table
- `date_of_birth` (DATE) - Patient's birth date
- `emergency_contact_name` (VARCHAR(200)) - Emergency contact
- `base_medical_history` (TEXT) - Initial medical history

**Relationships**:
- Many-to-one with Users
- One-to-many with FamilyMembers, Appointments, MedicalRecords, PatientMaterialAssignments

**Constraints**:
- Unique constraint on `user_id` (one patient per user)

### 4. FamilyMembers Table

**Purpose**: Family relationships and access permissions

**Key Fields**:
- `family_member_id` (UUID, PK) - Unique identifier
- `user_id` (UUID, FK) - Reference to Users table
- `patient_id` (UUID, FK) - Reference to Patients table
- `relationship` (VARCHAR(50)) - Relationship type (Parent, Spouse, Child)

**Relationships**:
- Many-to-one with Users and Patients
- Unique constraint on (user_id, patient_id) combination

### 5. Appointments Table

**Purpose**: Appointment scheduling and management

**Key Fields**:
- `appointment_id` (UUID, PK) - Unique identifier
- `specialist_id` (UUID, FK) - Reference to Specialists table
- `patient_id` (UUID, FK) - Reference to Patients table
- `start_datetime` (TIMESTAMP) - Appointment start time
- `end_datetime` (TIMESTAMP) - Appointment end time
- `status` (VARCHAR(20)) - Appointment status
- `appointment_type` (VARCHAR(50)) - Type of appointment

**Relationships**:
- Many-to-one with Specialists and Patients

**Constraints**:
- `end_datetime > start_datetime` - Valid time range
- Status must be one of: Pending, Confirmed, Canceled, Completed, NoShow

**Indexes**:
- Composite index on (start_datetime, end_datetime) for date range queries
- Indexes on specialist_id and patient_id for filtering

### 6. AvailabilityBlocks Table

**Purpose**: Specialist availability scheduling

**Key Fields**:
- `availability_block_id` (UUID, PK) - Unique identifier
- `specialist_id` (UUID, FK) - Reference to Specialists table
- `day_of_week` (INTEGER) - Day of week (1=Monday, 7=Sunday)
- `start_time` (TIME) - Start time
- `end_time` (TIME) - End time
- `exception_date` (DATE) - Override for specific dates

**Relationships**:
- Many-to-one with Specialists

**Constraints**:
- `day_of_week` between 1 and 7
- `end_time > start_time`

### 7. MedicalRecords Table

**Purpose**: Patient medical history and treatment records

**Key Fields**:
- `record_id` (UUID, PK) - Unique identifier
- `patient_id` (UUID, FK) - Reference to Patients table
- `specialist_id` (UUID, FK) - Reference to Specialists table
- `record_date` (DATE) - Date of the medical record
- `diagnosis` (TEXT) - Medical diagnosis
- `treatment` (TEXT) - Treatment provided
- `attached_files_json` (JSONB) - File attachments (PDFs, images)

**Relationships**:
- Many-to-one with Patients and Specialists

**Security**: Contains sensitive medical information requiring encryption

### 8. Templates Table

**Purpose**: Reusable medical document templates

**Key Fields**:
- `template_id` (UUID, PK) - Unique identifier
- `specialist_id` (UUID, FK) - Reference to Specialists table (optional)
- `template_name` (VARCHAR(200)) - Template name
- `content` (TEXT) - Template content (HTML/Markdown)
- `template_type` (VARCHAR(50)) - Template category
- `is_global` (BOOLEAN) - Available to all specialists

**Relationships**:
- Many-to-one with Specialists (optional)

### 9. EducationalMaterials Table

**Purpose**: Educational content management

**Key Fields**:
- `material_id` (UUID, PK) - Unique identifier
- `title` (VARCHAR(200)) - Material title
- `content_url` (TEXT) - Link to content (video, PDF, etc.)
- `material_type` (VARCHAR(50)) - Content type
- `publish_date` (DATE) - Publication date
- `specialist_id` (UUID, FK) - Reference to Specialists table (optional)

**Relationships**:
- Many-to-one with Specialists (optional)
- One-to-many with PatientMaterialAssignments

### 10. PatientMaterialAssignments Table

**Purpose**: Patient-specific educational content assignments

**Key Fields**:
- `assignment_id` (UUID, PK) - Unique identifier
- `patient_id` (UUID, FK) - Reference to Patients table
- `material_id` (UUID, FK) - Reference to EducationalMaterials table
- `assignment_date` (DATE) - Assignment date
- `specialist_comments` (TEXT) - Specialist notes

**Relationships**:
- Many-to-one with Patients and EducationalMaterials

**Constraints**:
- Unique constraint on (patient_id, material_id) - One assignment per patient per material

### 11. Notifications Table

**Purpose**: System notifications management

**Key Fields**:
- `notification_id` (UUID, PK) - Unique identifier
- `user_id` (UUID, FK) - Reference to Users table
- `title` (VARCHAR(200)) - Notification title
- `message` (TEXT) - Notification message
- `notification_type` (VARCHAR(50)) - Type of notification
- `is_read` (BOOLEAN) - Read status

**Relationships**:
- Many-to-one with Users

### 12. AuditLogs Table

**Purpose**: Track changes to sensitive data for compliance

**Key Fields**:
- `log_id` (UUID, PK) - Unique identifier
- `table_name` (VARCHAR(100)) - Affected table
- `record_id` (UUID) - Affected record ID
- `action` (VARCHAR(20)) - Action type (INSERT, UPDATE, DELETE)
- `old_values` (JSONB) - Previous values
- `new_values` (JSONB) - New values
- `user_id` (UUID, FK) - User who made the change

**Relationships**:
- Many-to-one with Users

## Data Relationships Diagram

```
Users (1) ←→ (1) Specialists
   ↓
   ↓ (1) ←→ (1) Patients
   ↓
   ↓ (1) ←→ (M) FamilyMembers
   ↓
   ↓ (1) ←→ (M) Notifications
   ↓
   ↓ (1) ←→ (M) AuditLogs

Specialists (1) ←→ (M) Appointments
Specialists (1) ←→ (M) AvailabilityBlocks
Specialists (1) ←→ (M) MedicalRecords
Specialists (1) ←→ (M) Templates
Specialists (1) ←→ (M) EducationalMaterials

Patients (1) ←→ (M) Appointments
Patients (1) ←→ (M) MedicalRecords
Patients (1) ←→ (M) PatientMaterialAssignments

EducationalMaterials (1) ←→ (M) PatientMaterialAssignments
```

## Security Considerations

### Data Protection
- **Password Hashing**: All passwords are hashed using bcrypt
- **Medical Data Encryption**: Sensitive medical records should be encrypted at rest
- **Audit Logging**: All changes to sensitive data are logged
- **Role-Based Access**: Users can only access data appropriate to their role

### Access Control
- **Admin**: Full access to all data and system functions
- **Specialist**: Access to their patients, appointments, and medical records
- **Patient**: Access to their own data and assigned educational materials
- **FamilyMember**: Limited access to associated patient's data

### Compliance
- **HIPAA Compliance**: Design supports HIPAA requirements for medical data
- **Audit Trails**: Complete audit logging for compliance reporting
- **Data Retention**: Configurable data retention policies

## Performance Optimizations

### Indexes
- Primary keys on all tables
- Foreign key indexes for relationship queries
- Composite indexes for common query patterns
- Date range indexes for appointment and medical record queries

### Query Optimization
- Efficient joins using indexed foreign keys
- Pagination support for large datasets
- Caching strategies for frequently accessed data

## Migration and Deployment

### Database Setup
1. Create PostgreSQL database
2. Enable UUID extension: `CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`
3. Run schema creation script
4. Create indexes for performance
5. Set up audit triggers

### Sample Data
- Admin user for initial access
- Sample specialist and patient accounts
- Template educational materials

## Backup and Recovery

### Backup Strategy
- Daily automated backups
- Point-in-time recovery capability
- Encrypted backup storage
- Regular backup testing

### Disaster Recovery
- Multi-region backup replication
- Automated failover procedures
- Data integrity verification

## Monitoring and Maintenance

### Performance Monitoring
- Query performance tracking
- Index usage monitoring
- Connection pool monitoring
- Slow query identification

### Maintenance Tasks
- Regular index maintenance
- Statistics updates
- Vacuum operations
- Log rotation and cleanup

## Future Enhancements

### Potential Additions
- **Billing System**: Payment processing and invoicing
- **Insurance Integration**: Insurance claim management
- **Telemedicine**: Video consultation support
- **Mobile App**: Patient mobile application
- **Analytics**: Advanced reporting and analytics
- **Integration APIs**: Third-party system integrations

### Scalability Considerations
- **Sharding**: Horizontal partitioning for large datasets
- **Read Replicas**: Separate read/write databases
- **Caching Layer**: Redis for frequently accessed data
- **Microservices**: Service-oriented architecture 