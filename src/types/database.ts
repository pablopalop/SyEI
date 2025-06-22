// SyEI - Database Types
// TypeScript interfaces for the Holistic Medical Center database schema

export interface User {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  passwordHash: string;
  role: UserRole;
  registrationDate: Date;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
}

export interface Specialist {
  id: string;
  userId: string;
  specialty: string;
  description?: string;
  phoneNumber?: string;
  professionalLicense?: string;
  bio?: string;
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
  
  // Relations
  user?: User;
  appointments?: Appointment[];
  availabilityBlocks?: AvailabilityBlock[];
  medicalRecords?: MedicalRecord[];
  templates?: Template[];
  educationalMaterials?: EducationalMaterial[];
}

export interface Patient {
  id: string;
  userId: string;
  dateOfBirth: Date;
  address?: string;
  emergencyPhone?: string;
  emergencyContactName?: string;
  baseMedicalHistory?: string;
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
  
  // Relations
  user?: User;
  familyMembers?: FamilyMember[];
  appointments?: Appointment[];
  medicalRecords?: MedicalRecord[];
  materialAssignments?: PatientMaterialAssignment[];
}

export interface FamilyMember {
  id: string;
  userId: string;
  patientId: string;
  relationship: string;
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
  
  // Relations
  user?: User;
  patient?: Patient;
}

export interface Appointment {
  id: string;
  specialistId: string;
  patientId: string;
  startDateTime: Date;
  endDateTime: Date;
  status: AppointmentStatus;
  appointmentType: string;
  internalNotes?: string;
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
  
  // Relations
  specialist?: Specialist;
  patient?: Patient;
}

export interface AvailabilityBlock {
  id: string;
  specialistId: string;
  dayOfWeek: number; // 1=Monday, 7=Sunday
  startTime: Date;
  endTime: Date;
  isActive: boolean;
  exceptionDate?: Date;
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
  
  // Relations
  specialist?: Specialist;
}

export interface MedicalRecord {
  id: string;
  patientId: string;
  specialistId: string;
  recordDate: Date;
  diagnosis?: string;
  treatment?: string;
  progressNotes?: string;
  attachedFilesJson?: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
  
  // Relations
  patient?: Patient;
  specialist?: Specialist;
}

export interface Template {
  id: string;
  specialistId?: string;
  templateName: string;
  content: string;
  templateType: string;
  isGlobal: boolean;
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
  
  // Relations
  specialist?: Specialist;
}

export interface EducationalMaterial {
  id: string;
  title: string;
  description?: string;
  contentUrl: string;
  materialType: string;
  publishDate: Date;
  specialistId?: string;
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
  
  // Relations
  specialist?: Specialist;
  materialAssignments?: PatientMaterialAssignment[];
}

export interface PatientMaterialAssignment {
  id: string;
  patientId: string;
  materialId: string;
  assignmentDate: Date;
  specialistComments?: string;
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
  
  // Relations
  patient?: Patient;
  material?: EducationalMaterial;
}

export interface Notification {
  id: string;
  userId: string;
  title: string;
  message: string;
  notificationType: string;
  isRead: boolean;
  createdAt: Date;
  readAt?: Date;
  
  // Relations
  user?: User;
}

export interface AuditLog {
  id: string;
  tableName: string;
  recordId: string;
  action: 'INSERT' | 'UPDATE' | 'DELETE';
  oldValues?: Record<string, any>;
  newValues?: Record<string, any>;
  userId?: string;
  timestamp: Date;
  
  // Relations
  user?: User;
}

// =====================================================
// ENUMS
// =====================================================

export enum UserRole {
  Admin = 'Admin',
  Specialist = 'Specialist',
  Patient = 'Patient',
  FamilyMember = 'FamilyMember'
}

export enum AppointmentStatus {
  Pending = 'Pending',
  Confirmed = 'Confirmed',
  Canceled = 'Canceled',
  Completed = 'Completed',
  NoShow = 'NoShow'
}

// =====================================================
// CREATE/UPDATE DTOs
// =====================================================

export interface CreateUserDto {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  role: UserRole;
}

export interface UpdateUserDto {
  firstName?: string;
  lastName?: string;
  email?: string;
  isActive?: boolean;
}

export interface CreateSpecialistDto {
  userId: string;
  specialty: string;
  description?: string;
  phoneNumber?: string;
  professionalLicense?: string;
  bio?: string;
}

export interface UpdateSpecialistDto {
  specialty?: string;
  description?: string;
  phoneNumber?: string;
  professionalLicense?: string;
  bio?: string;
}

export interface CreatePatientDto {
  userId: string;
  dateOfBirth: Date;
  address?: string;
  emergencyPhone?: string;
  emergencyContactName?: string;
  baseMedicalHistory?: string;
}

export interface UpdatePatientDto {
  dateOfBirth?: Date;
  address?: string;
  emergencyPhone?: string;
  emergencyContactName?: string;
  baseMedicalHistory?: string;
}

export interface CreateAppointmentDto {
  specialistId: string;
  patientId: string;
  startDateTime: Date;
  endDateTime: Date;
  appointmentType: string;
  internalNotes?: string;
}

export interface UpdateAppointmentDto {
  startDateTime?: Date;
  endDateTime?: Date;
  status?: AppointmentStatus;
  appointmentType?: string;
  internalNotes?: string;
}

export interface CreateMedicalRecordDto {
  patientId: string;
  specialistId: string;
  recordDate?: Date;
  diagnosis?: string;
  treatment?: string;
  progressNotes?: string;
  attachedFilesJson?: Record<string, any>;
}

export interface UpdateMedicalRecordDto {
  recordDate?: Date;
  diagnosis?: string;
  treatment?: string;
  progressNotes?: string;
  attachedFilesJson?: Record<string, any>;
}

// =====================================================
// QUERY TYPES
// =====================================================

export interface UserFilters {
  role?: UserRole;
  isActive?: boolean;
  search?: string;
}

export interface AppointmentFilters {
  specialistId?: string;
  patientId?: string;
  status?: AppointmentStatus;
  startDate?: Date;
  endDate?: Date;
}

export interface MedicalRecordFilters {
  patientId?: string;
  specialistId?: string;
  startDate?: Date;
  endDate?: Date;
}

// =====================================================
// RESPONSE TYPES
// =====================================================

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface LoginResponse {
  user: User;
  token: string;
  refreshToken: string;
}

export interface DashboardStats {
  totalPatients: number;
  totalSpecialists: number;
  totalAppointments: number;
  pendingAppointments: number;
  completedAppointments: number;
  todayAppointments: number;
} 