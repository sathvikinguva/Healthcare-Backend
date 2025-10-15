from django.contrib import admin
from .models import Patient, Doctor, PatientDoctorMapping


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin configuration for Patient model
    """
    list_display = ('name', 'email', 'phone', 'gender', 'date_of_birth', 'created_by', 'created_at')
    list_filter = ('gender', 'created_at', 'created_by')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Doctor model
    """
    list_display = ('name', 'email', 'specialization', 'years_of_experience', 'consultation_fee', 'created_by', 'created_at')
    list_filter = ('specialization', 'created_at', 'created_by')
    search_fields = ('name', 'email', 'specialization', 'qualification')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    """
    Admin configuration for PatientDoctorMapping model
    """
    list_display = ('patient', 'doctor', 'assigned_date', 'is_active', 'created_by')
    list_filter = ('is_active', 'assigned_date', 'created_by')
    search_fields = ('patient__name', 'doctor__name', 'patient__email', 'doctor__email')
    readonly_fields = ('assigned_date',)
    ordering = ('-assigned_date',)
