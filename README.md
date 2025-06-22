# SyEI - Holistic Medical Center Backoffice

A comprehensive backoffice system for managing a holistic medical center with multiple professionals and user profiles.

## Features

- **User Management**: Multi-role user system (Admin, Specialist, Patient, FamilyMember)
- **Appointment Management**: Complete calendar and scheduling system
- **Medical Records**: Secure patient medical history and treatment tracking
- **Educational Materials**: Content management and patient assignment system
- **Specialist Management**: Professional profiles and availability tracking
- **Family Member Integration**: Support for family relationships and access

## Database Structure

The system uses a relational database with the following core entities:

### Core Tables
- **Users**: Base user accounts with role-based access
- **Specialists**: Medical professionals with specialties
- **Patients**: Patient profiles and medical information
- **FamilyMembers**: Family relationships and access

### Management Tables
- **Appointments**: Scheduling and appointment tracking
- **AvailabilityBlocks**: Specialist availability management
- **MedicalRecords**: Patient medical history and treatments
- **Templates**: Reusable medical document templates
- **EducationalMaterials**: Educational content management
- **PatientMaterialAssignments**: Patient-specific content assignments

## Technology Stack

- Database: PostgreSQL (recommended) or SQLite for development
- Backend: Node.js with Express or Python with Django/FastAPI
- Frontend: React/Vue.js with modern UI components
- Authentication: JWT-based with role-based access control

## Getting Started

1. Set up the database using the provided schema
2. Configure environment variables
3. Install dependencies
4. Run migrations
5. Start the development server

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- Audit logging for sensitive operations
- Data encryption for medical records