from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model
    """
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
    
    def validate_email(self, value):
        """
        Validate that email is unique for patients created by the same user
        """
        user = self.context['request'].user
        patient_id = self.instance.id if self.instance else None
        
        if Patient.objects.filter(
            email=value,
            created_by=user
        ).exclude(id=patient_id).exists():
            raise serializers.ValidationError("A patient with this email already exists.")
        return value


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model
    """
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
    
    def validate_email(self, value):
        """
        Validate that email is unique for doctors
        """
        doctor_id = self.instance.id if self.instance else None
        
        if Doctor.objects.filter(email=value).exclude(id=doctor_id).exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value
    
    def validate_years_of_experience(self, value):
        """
        Validate years of experience
        """
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        if value > 50:
            raise serializers.ValidationError("Years of experience seems too high.")
        return value
    
    def validate_consultation_fee(self, value):
        """
        Validate consultation fee
        """
        if value <= 0:
            raise serializers.ValidationError("Consultation fee must be positive.")
        return value


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for PatientDoctorMapping model
    """
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    patient_email = serializers.CharField(source='patient.email', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'assigned_date', 'patient_name', 
                           'patient_email', 'doctor_name', 'doctor_specialization')
    
    def validate(self, data):
        """
        Validate that the patient and doctor exist and belong to the user
        """
        user = self.context['request'].user
        patient = data.get('patient')
        doctor = data.get('doctor')
        
        # Check if patient belongs to the user
        if patient and patient.created_by != user:
            raise serializers.ValidationError("You can only assign doctors to your own patients.")
        
        # Check if mapping already exists
        if PatientDoctorMapping.objects.filter(
            patient=patient,
            doctor=doctor,
            is_active=True
        ).exists():
            raise serializers.ValidationError("This patient is already assigned to this doctor.")
        
        return data


class PatientDoctorMappingListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing patient-doctor mappings with detailed information
    """
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = '__all__'