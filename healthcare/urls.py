from django.urls import path
from . import views

app_name = 'healthcare'

urlpatterns = [
    # Patient URLs
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    
    # Doctor URLs
    path('doctors/', views.DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    
    # Patient-Doctor Mapping URLs
    path('mappings/', views.assign_doctor_to_patient, name='assign-doctor'),
    path('mappings/list/', views.list_patient_doctor_mappings, name='list-mappings'),
    path('mappings/<int:patient_id>/', views.get_patient_doctors, name='patient-doctors'),
    path('mappings/remove/<int:mapping_id>/', views.remove_doctor_from_patient, name='remove-mapping'),
]