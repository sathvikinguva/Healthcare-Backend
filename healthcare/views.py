from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    PatientSerializer, 
    DoctorSerializer, 
    PatientDoctorMappingSerializer,
    PatientDoctorMappingListSerializer
)


# Patient Management Views
class PatientListCreateView(generics.ListCreateAPIView):
    """
    List all patients for authenticated user or create a new patient
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a patient
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)


# Doctor Management Views
class DoctorListCreateView(generics.ListCreateAPIView):
    """
    List all doctors or create a new doctor
    """
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return all doctors (not filtered by creator) as mentioned in requirements
        return Doctor.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a doctor
    """
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    
    def get_object(self):
        """
        Only allow updates/deletes for doctors created by the current user
        """
        obj = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.created_by != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You can only modify doctors you created.")
        return obj


# Patient-Doctor Mapping Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_doctor_to_patient(request):
    """
    Assign a doctor to a patient
    """
    try:
        serializer = PatientDoctorMappingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            mapping = serializer.save(created_by=request.user)
            response_serializer = PatientDoctorMappingListSerializer(mapping)
            return Response({
                'message': 'Doctor assigned to patient successfully',
                'mapping': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': 'Assignment failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_patient_doctor_mappings(request):
    """
    List all patient-doctor mappings for the authenticated user
    """
    try:
        mappings = PatientDoctorMapping.objects.filter(
            created_by=request.user,
            is_active=True
        )
        serializer = PatientDoctorMappingListSerializer(mappings, many=True)
        return Response({
            'mappings': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_doctors(request, patient_id):
    """
    Get all doctors assigned to a specific patient
    """
    try:
        # Verify patient belongs to user
        patient = get_object_or_404(Patient, id=patient_id, created_by=request.user)
        
        mappings = PatientDoctorMapping.objects.filter(
            patient=patient,
            is_active=True
        )
        serializer = PatientDoctorMappingListSerializer(mappings, many=True)
        return Response({
            'patient': {
                'id': patient.id,
                'name': patient.name,
                'email': patient.email
            },
            'assigned_doctors': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_doctor_from_patient(request, mapping_id):
    """
    Remove a doctor from a patient (deactivate mapping)
    """
    try:
        mapping = get_object_or_404(
            PatientDoctorMapping, 
            id=mapping_id, 
            created_by=request.user,
            is_active=True
        )
        
        mapping.is_active = False
        mapping.save()
        
        return Response({
            'message': 'Doctor removed from patient successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Internal server error',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
